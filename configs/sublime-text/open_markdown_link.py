import sublime
import sublime_plugin

SELECTOR = "markup.underline.link"

class OpenMarkdownLinkCommand(sublime_plugin.TextCommand):
    """
    This command opens markdown links:
    - local files are opened it in a new tab;
    - http(s) links are opened in the default browser.
    """
    def run(self, edit):
        v = self.view
        w = v.window()
        for i, sel in enumerate(v.sel(), 1):
            pt = sel.begin()

            if not v.match_selector(pt, SELECTOR):
                continue

            # Find the smallest region for the selector
            regions = [r for r in v.find_by_selector(SELECTOR) if r.contains(pt)]
            if not regions:
                continue
            target = min(regions, key=lambda r: r.size())

            link = v.substr(target)
            if link.lower().startswith(("http://", "https://")):
                w.run_command("open_url", {"url": link})
            else:
                w.open_file(link)
