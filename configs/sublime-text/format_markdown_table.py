import re
import sublime
import sublime_plugin

from typing import Optional


TABLE_SEP_RE = re.compile(r"^(\|\s*-+\s*)+(\|\s*)?$")


def line_text(view: sublime.View, row: int) -> str:
    """Return the full text of the given row without trailing newline."""
    pt = view.text_point(row, 0)
    return view.substr(view.line(pt))


def is_separator_line(text: str) -> bool:
    """True if line is a markdown table separator like `|--|--|`."""
    return bool(TABLE_SEP_RE.match(text))


def is_table_line(text: str) -> bool:
    """True if a line belongs to a markdown table."""
    return text.startswith("|")


def find_table_region(view: sublime.View, pt: int) -> Optional[sublime.Region]:
    """
    Find the contiguous markdown table block enclosing the caret point.
    Returns a Region spanning the table, or None if not found.
    """

    row, _ = view.rowcol(pt)
    total_rows, _ = view.rowcol(view.size())

    # If the current line isn't table-ish, early exit
    cur_text = line_text(view, row)
    if not is_table_line(cur_text):
        return None

    # Expand upwards
    start_row = row
    r = row - 1
    while r >= 0:
        t = line_text(view, r)
        if not is_table_line(t):
            break
        start_row = r
        r -= 1

    # Expand downwards
    end_row = row
    r = row + 1
    while r <= total_rows:
        t = line_text(view, r)
        if not is_table_line(t):
            break
        end_row = r
        r += 1

    # Validate that the second row is a separator
    if end_row - start_row < 1:
        return None
    if not is_separator_line(line_text(view, start_row + 1)):
        return None

    start_pt = view.text_point(start_row, 0)
    end_pt = view.full_line(view.text_point(end_row, 0)).end()
    return sublime.Region(start_pt, end_pt)


def format_table(view: sublime.View, edit: sublime.Edit, region: sublime.Region) -> None:
    """Format the provided table and update the document in-place."""

    lines = [view.substr(line) for line in view.lines(region)]

    # Build a 2d-array of cells
    rows = []
    for line in lines:
        s = line.rstrip()
        if s.startswith('|'):
            s = s[1:]
        if s.endswith('|'):
            s = s[:-1]
        cells = [c.strip() for c in s.split('|')]
        rows.append(cells)

    cols_num = max(len(r) for r in rows)

    # Compute width for each column (3 is a minimum)
    widths = [3] * cols_num
    for col_num in range(cols_num):
        max_len = 0
        for row_num, row in enumerate(rows):
            if row_num == 1:
                continue
            if col_num < len(row):
                max_len = max(max_len, len(row[col_num]))
        widths[col_num] = max(3, max_len)

    # Build formatted rows
    formatted = []
    for row_num, row in enumerate(rows):
        row = row + [""] * (cols_num - len(row))
        if row_num == 1:  # separator
            parts = [" " + ("-" * widths[c]) + " " for c in range(cols_num)]
        else:
            parts = [" " + row[c].ljust(widths[c]) + " " for c in range(cols_num)]
        formatted.append("|" + "|".join(parts) + "|")

    view.replace(edit, region, "\n".join(formatted) + "\n")


class FormatMarkdownTableCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        sel = self.view.sel()
        if not sel:
            return

        caret = sel[0].begin()
        region = find_table_region(self.view, caret)
        if not region:
            return

        format_table(self.view, edit, region)
