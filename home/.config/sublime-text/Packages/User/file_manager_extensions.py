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
    """

    def run(self, edit, text):
        region = sublime.Region(0, self.view.size())
        self.view.replace(edit, region, text)
        region = sublime.Region(self.view.size(), self.view.size())
        self.view.sel().clear()
        self.view.sel().add(region)


class PathInput:
    """
    Interactive path input panel with tab-completion support.
    Provides filesystem navigation and completion for both files and directories.
    """

    def __init__(
        self, window, caption, initial_text, on_done, *, include_files,
        base_dir, select=None, on_cancel=None, case_sensitive=True,
    ):
        self.window = window or sublime.active_window()
        self.caption = caption
        self.on_done = on_done
        self.on_cancel = on_cancel
        self.include_files = include_files
        self.case_sensitive = case_sensitive
        self.base_reference = os.path.abspath(base_dir or os.getcwd())
        self.ignore_events = False
        self.value = initial_text
        self.completions = []
        self.current_completion = None
        self.index = -1
        self.separators = self._available_separators()
        self.view = self.window.show_input_panel(caption, initial_text,
            self._handle_done, self._handle_change, self._cancel)
        self.view.set_name("FileManager::PathInput")
        self.view.settings().set("tab_completion", False)

        if select:
            sublime.set_timeout(lambda: self._select_range(*select), 0)

    def _select_range(self, start, end):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(start, end))

    def _available_separators(self):
        seps = {"/", os.path.sep}
        if os.path.altsep:
            seps.add(os.path.altsep)
        return list(seps)

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
        value = self.value.strip() if self.value is not None else ""
        if not value:
            return
        self.on_done(value)

    def _cancel(self):
        if self.on_cancel:
            self.on_cancel()

    def _replace_text(self, text):
        self.ignore_events = True
        self.view.run_command("fm_replace_input", {"text": text})
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
        """
        Find filesystem entries matching the partial input.
        Returns folders first, then files, with trailing separator on folders.
        """
        base, prefix = self._split_input(text)
        directory = self._resolve_directory(base)

        try:
            entries = sorted(os.listdir(directory))
        except OSError:
            return []

        prefix_cmp = prefix if self.case_sensitive else prefix.lower()
        folders, files = [], []

        for entry in entries:
            cmp_name = entry if self.case_sensitive else entry.lower()
            if not cmp_name.startswith(prefix_cmp):
                continue
            full = os.path.join(directory, entry)
            if os.path.isdir(full):
                folders.append(entry)
            elif self.include_files:
                files.append(entry)

        ordered = folders + files
        if not ordered:
            return []

        suffix = os.path.sep
        results = []
        for entry in ordered:
            candidate = base + entry
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                candidate += suffix
            results.append(candidate)
        return results

    def _split_input(self, text):
        """Split input into base directory and filename prefix for completion."""
        last_index = -1
        for sep in self.separators:
            index = text.rfind(sep)
            if index > last_index:
                last_index = index
        if last_index == -1:
            return "", text
        return text[: last_index + 1], text[last_index + 1 :]

    def _resolve_directory(self, base_text):
        """Convert base path text to absolute directory for listing entries."""
        raw = base_text.rstrip("/\\")
        if not raw:
            raw = self.base_reference
        raw = os.path.expanduser(os.path.expandvars(raw))
        if not os.path.isabs(raw):
            raw = os.path.join(self.base_reference, raw)
        return os.path.normpath(raw)


class FmMoveCommand(sublime_plugin.WindowCommand):
    """
    Move files or folders to a different directory with tab-completion.
    """

    def run(self, paths=None):
        targets = self._collect_paths(paths)
        if not targets:
            sublime.error_message("FileManager: nothing to move.")
            return
        self.targets = targets
        initial_dir = self._dir_with_sep(os.path.dirname(targets[0]))
        self.input = PathInput(
            self.window,
            "Move to directory:",
            initial_dir,
            self._on_done,
            include_files=False,
            base_dir=os.path.dirname(targets[0]),
        )

    def _collect_paths(self, paths):
        items = paths or []
        if not items:
            view = self.window.active_view()
            if view and view.file_name():
                items = [view.file_name()]
        return [os.path.abspath(item) for item in items if item]

    def _dir_with_sep(self, path):
        if not path:
            path = os.getcwd()
        if path.endswith(os.path.sep):
            return path
        if os.path.altsep and path.endswith(os.path.altsep):
            return path
        return path + os.path.sep

    def _on_done(self, text):
        """Execute move operation after user confirms destination."""
        destination = resolve_path(text, os.path.dirname(self.targets[0]))
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


class FmDuplicateCommand(sublime_plugin.WindowCommand):
    """
    Duplicate a file with a new name, optionally overwriting existing files.
    """

    def run(self, paths=None):
        path = self._target_path(paths)
        if not path:
            sublime.error_message("FileManager: nothing to duplicate.")
            return
        if not os.path.isfile(path):
            sublime.error_message("FileManager: duplicate only works on files.")
            return
        self.origin = os.path.abspath(path)
        initial_text = self.origin
        dirname = os.path.dirname(initial_text)
        basename = os.path.basename(initial_text)
        name_only = os.path.splitext(basename)[0]
        start = len(dirname) + 1 if dirname else 0
        end = start + len(name_only)
        self.input = PathInput(
            self.window,
            "Duplicate to:",
            initial_text,
            self._on_done,
            include_files=False,
            base_dir=dirname or os.getcwd(),
            select=(start, end),
        )

    def _target_path(self, paths):
        if paths:
            return paths[0]
        view = self.window.active_view()
        return view.file_name() if view else None

    def is_visible(self, paths=None):
        if paths:
            return os.path.isfile(paths[0])
        return True

    def _on_done(self, text):
        """Execute duplication after user confirms destination."""
        destination = resolve_path(text, os.path.dirname(self.origin))
        if destination is None:
            sublime.error_message("FileManager: invalid destination.")
            return
        source = self.origin

        # If user typed trailing slash or destination is existing dir,
        # use source filename inside that directory
        treat_as_dir = text.endswith(os.path.sep) or os.path.isdir(destination)
        if treat_as_dir:
            destination = os.path.join(destination, os.path.basename(source))

        if os.path.abspath(source) == os.path.abspath(destination):
            sublime.error_message("Source and destination are the same.")
            return

        try:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
        except OSError as exc:
            sublime.error_message("Unable to create folder: {}".format(exc))
            return

        if os.path.exists(destination):
            choice = sublime.yes_no_cancel_dialog(
                "{} exists. Overwrite?".format(destination),
                "Overwrite",
                "Open Existing",
            )
            if choice == sublime.DIALOG_CANCEL:
                return
            if choice == sublime.DIALOG_NO:
                self.window.open_file(destination)
                return
            try:
                os.remove(destination)
            except OSError as exc:
                sublime.error_message("Unable to remove target: {}".format(exc))
                return

        try:
            shutil.copy2(source, destination)
        except OSError as exc:
            sublime.error_message("Unable to duplicate file: {}".format(exc))
            return

        self.window.open_file(destination)
        self.window.run_command("refresh_folder_list")
