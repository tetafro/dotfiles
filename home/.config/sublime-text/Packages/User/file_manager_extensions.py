# Extensions to the standard sidebar file manager. Adds Duplicate and Move (with
# tab completion) commands.
import os
import shutil
import sublime
import sublime_plugin


def resolve_path(raw, relative_to):
    """
    Convert user input to an absolute normalized path.
    Handles environment variables, tilde expansion, and relative paths.
    """

    if raw is None:
        return None
    text = raw.strip()
    if not text:
        return None
    expanded = os.path.expanduser(os.path.expandvars(text))
    if not os.path.isabs(expanded):
        base = relative_to or os.getcwd()
        expanded = os.path.join(base, expanded)
    return os.path.normpath(expanded)


class FmReplaceInputCommand(sublime_plugin.TextCommand):
    """
    Helper command to replace entire input panel content and move cursor to end.
    Command name: fm_replace_input (derived from the class name).
    """

    def run(self, edit, text):
        region = sublime.Region(0, self.view.size())
        self.view.replace(edit, region, text)
        region = sublime.Region(self.view.size(), self.view.size())
        self.view.sel().clear()
        self.view.sel().add(region)


class FmMoveCommand(sublime_plugin.WindowCommand):
    """
    Move files or folders to a different directory with tab-completion.
    Command name: fm_move (derived from the class name).
    """

    def run(self, paths=None):
        targets = self._collect_paths(paths)
        if not targets:
            sublime.error_message("FileManager: nothing to move.")
            return
        self.targets = targets
        init_dir = os.path.dirname(targets[0])
        if init_dir.endswith(os.path.sep):
            init_dir =+ os.path.sep
        self.base_reference = os.path.abspath(os.path.dirname(targets[0]))
        self.ignore_events = False
        self.value = init_dir
        self.completions = []
        self.current_completion = None
        self.index = -1
        self.input_view = self.window.show_input_panel("Move to directory:",
            init_dir, self._handle_done, self._handle_change, self._cancel)
        self.input_view.set_name("FileManager::PathInput")
        self.input_view.settings().set("tab_completion", False)

    def _collect_paths(self, paths):
        if not paths:
            view = self.window.active_view()
            if view and view.file_name():
                paths = [view.file_name()]
        return [os.path.abspath(path) for path in paths if path]

    def _handle_change(self, text):
        """Handle input changes. Tab key triggers path completion."""

        if self.ignore_events:
            return
        if text.endswith("\t"):
            trimmed = text[:-1]
            self._replace_text(trimmed)
            self._complete(trimmed)
            return
        self.value = text
        self.completions = []
        self.current_completion = None
        self.index = -1

    def _handle_done(self, text):
        """Execute move operation after user confirms destination."""

        value = self.value.strip() if self.value is not None else ""
        if not value:
            return

        destination = resolve_path(value, os.path.dirname(self.targets[0]))
        if destination is None:
            sublime.error_message("FileManager: invalid destination.")
            return
        try:
            os.makedirs(destination, exist_ok=True)
        except OSError as exc:
            sublime.error_message("Unable to create {}: {}".format(destination, exc))
            return

        for source in self.targets:
            new_name = os.path.join(destination, os.path.basename(source))
            if os.path.abspath(source) == os.path.abspath(new_name):
                continue
            if os.path.exists(new_name):
                sublime.error_message("{} already exists.".format(new_name))
                return
            try:
                os.rename(source, new_name)
            except OSError as exc:
                sublime.error_message(
                    "Unable to move {} to {}: {}".format(source, new_name, exc)
                )
                return
            # Update open views to point to new location
            view = self.window.find_open_file(source)
            if view:
                view.retarget(new_name)

        self.window.run_command("refresh_folder_list")

    def _cancel(self):
        pass

    def _replace_text(self, text):
        self.ignore_events = True
        self.input_view.run_command("fm_replace_input", {"text": text})
        self.ignore_events = False
        self.value = text

    def _complete(self, text):
        """Cycle through path completions. Repeated tabs cycle through matches."""

        if self.completions and text == self.current_completion:
            self.index = (self.index + 1) % len(self.completions)
        else:
            items = self._gather_completions(text)
            if not items:
                return
            self.completions = items
            self.index = 0
        completed = self.completions[self.index]
        self.current_completion = completed
        self._replace_text(completed)

    def _gather_completions(self, text):
        """Find filesystem directories matching the partial input."""

        base, prefix = self._split_input(text)
        directory = self._resolve_directory(base)

        try:
            entries = sorted(os.listdir(directory))
        except OSError:
            return []

        folders = []
        for entry in entries:
            if not entry.startswith(prefix):
                continue
            full = os.path.join(directory, entry)
            if os.path.isdir(full):
                folders.append(entry)

        if not folders:
            return []

        suffix = os.path.sep
        results = []
        for folder in folders:
            candidate = base + folder + suffix
            results.append(candidate)
        return results

    def _split_input(self, text):
        """Split input into base directory and filename prefix for completion."""

        index = text.rfind(os.path.sep)
        if index == -1:
            return "", text
        return text[:index+1], text[index+1:]

    def _resolve_directory(self, base_text):
        """Convert base path text to absolute directory for listing entries."""

        raw = base_text.rstrip("/\\")
        if not raw:
            raw = self.base_reference
        raw = os.path.expanduser(os.path.expandvars(raw))
        if not os.path.isabs(raw):
            raw = os.path.join(self.base_reference, raw)
        return os.path.normpath(raw)


class FmDuplicateCommand(sublime_plugin.WindowCommand):
    """
    Duplicate a file by adding " (copy)" to the filename.
    Command name: fm_duplicate (derived from the class name).
    """

    def run(self, paths=None):
        if not paths:
            sublime.error_message("FileManager: nothing to duplicate.")
            return
        path = paths[0]
        if not os.path.isfile(path):
            sublime.error_message("FileManager: duplicate only works on files.")
            return

        src = os.path.abspath(path)
        dst = self._generate_copy_name(src)

        try:
            shutil.copy2(src, dst)
        except OSError as exc:
            sublime.error_message("Unable to duplicate file: {}".format(exc))
            return
        self.window.run_command("refresh_folder_list")

    def is_visible(self, paths=None):
        """Hide the command for directories."""
        if paths:
            return os.path.isfile(paths[0])
        return True

    def _generate_copy_name(self, path):
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)

        cnt = 2
        dst = os.path.join(dirname, "{} ({}){}".format(name, cnt, ext))
        while os.path.exists(dst):
            cnt += 1
            dst = os.path.join(dirname, "{} ({}){}".format(name, cnt, ext))
        return dst
