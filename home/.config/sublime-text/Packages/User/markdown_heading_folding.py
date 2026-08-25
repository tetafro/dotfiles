import sublime
import sublime_plugin


class MarkdownFoldByHeaderLevelCommand(sublime_plugin.TextCommand):
    """
    Fold Markdown sections using header levels instead of indentation.
    """

    def run(self, edit, level):
        # Each level replaces the current fold state
        self.view.unfold(sublime.Region(0, self.view.size()))
        if level == 0:
            return

        # Find all headers
        headers = []
        for header_level in range(1, 7):
            selector = "markup.heading.{}".format(header_level)
            for region in self.view.find_by_selector(selector):
                lines = self.view.line(region)
                headers.append((lines.begin(), lines.end(), header_level))
        headers.sort()

        # Find which headers should be folded
        folds = []
        for index, (_, header_end, header_level) in enumerate(headers):
            if header_level != level:
                continue
            # Stop at the next sibling header or the next ancestor header
            fold_end = self.view.size()
            for next_start, _, next_level in headers[index + 1:]:
                if next_level <= header_level:
                    fold_end = self.view.line(next_start - 1).end()
                    break
            # If the header has any content - fold it
            if fold_end > header_end:
                folds.append(sublime.Region(header_end, fold_end))

        # Fold all found headers
        self.view.fold(folds)

    def is_enabled(self, level):
        return self.view.match_selector(0, "text.html.markdown")
