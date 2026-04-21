import os
import re
import sublime
import sublime_plugin


class SaveMarkdownCommand(sublime_plugin.TextCommand):
    """
    Save the active markdown file using a filename derived from its first H1.
    """

    def run(self, edit):
        view = self.view
        window = view.window()
        if window is None:
            debug("no active window")
            return
        if view.settings().get("is_widget"):
            debug("active view is not an editor")
            return

        # Get the filename from the header line
        first_line = view.substr(view.line(0))
        if not first_line.startswith("# "):
            debug("first line is not a level-1 markdown header")
            return
        target_file = filename(first_line)
        if not target_file:
            debug("filename is empty after normalization")
            return
        target_file += ".md"

        # Build the full path
        current_file = view.file_name()
        if current_file:
            directory = os.path.dirname(current_file)
        else:
            # Default directory is used when a new file was created in
            # a directory (for example, by right-clicking it in the filetree)
            directory = view.settings().get("default_dir")
            if not directory:
                folders = window.folders()
                if not folders:
                    debug("cannot save new file: window has no folders")
                    return
                directory = folders[0]
        target_file = os.path.join(directory, target_file)

        # The filename is already correct, just save the file
        if current_file and os.path.abspath(current_file) == os.path.abspath(target_file):
            sublime.set_timeout(lambda: self._save(window), 0)
            return

        if os.path.exists(target_file):
            debug("target already exists: {}".format(target_file))
            return

        if current_file:
            try:
                os.rename(current_file, target_file)
            except OSError as exc:
                debug("rename failed: {}".format(exc))
                return

        view.retarget(target_file)
        sublime.set_timeout(lambda: self._save(window), 0)

    def _save(self, window):
        window.run_command("save")
        window.run_command("refresh_folder_list")


def filename(first_line: str):
    fname = first_line[2:] # remove "# "
    fname = fname.strip()
    fname = fname.lower()
    fname = fname.replace(" ", "-")
    fname = "".join(ch for ch in fname if ch.isalnum() or ch == "-")
    return fname


def debug(message: str):
    print("save_markdown_from_header: {}".format(message))
