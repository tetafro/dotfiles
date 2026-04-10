import sublime
import sublime_plugin


class SingleTrailingNewline(sublime_plugin.EventListener):
    """
    Ensures files end with exactly one newline on save.

    `EventListener` cannot create `edit` objects directly, so it delegates
    to a TextCommand which receives a proper `edit` object from Sublime.
    """

    def on_pre_save(self, view):
        view.run_command("single_trailing_newline_fix")


class SingleTrailingNewlineFixCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.size() < 1:
            return

        # Find last non-whitespace character
        last_char = self.view.size() - 1
        while last_char >= 0 and self.view.substr(last_char).isspace():
            last_char -= 1

        # Remove trailing whitespace and add single newline
        self.view.erase(edit, sublime.Region(last_char + 1, self.view.size()))
        self.view.insert(edit, self.view.size(), "\n")
