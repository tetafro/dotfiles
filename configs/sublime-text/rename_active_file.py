import sublime
import sublime_plugin

class RenameActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.active_view()
        if v and v.file_name():
            self.window.run_command("rename_path", {"paths": [v.file_name()]})
        else:
            sublime.status_message("No file to rename.")
