import sublime
import sublime_plugin

class RenameActiveFileCommand(sublime_plugin.WindowCommand):
    """
    Rename a file when it is focused in the sidebar.
    Does't work for directories.
    """

    def run(self):
        v = self.window.active_view()
        if v and v.file_name():
            self.window.run_command("rename_path", {"paths": [v.file_name()]})
        else:
            sublime.status_message("No file to rename.")
