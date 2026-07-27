from datetime import date

import sublime_plugin


class InsertCurrentDateCommand(sublime_plugin.TextCommand):
    """
    Insert current date in the YYYY-MM-DD format.
    """

    def run(self, edit):
        today = date.today().isoformat()
        for region in reversed(list(self.view.sel())):
            self.view.replace(edit, region, today)
