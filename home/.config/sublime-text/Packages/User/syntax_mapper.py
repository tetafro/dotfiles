import sublime
import sublime_plugin
import os
from fnmatch import fnmatch


PATTERNS = {
    'yml': 'Packages/YAML/YAML.sublime-syntax',
    'yaml': 'Packages/YAML/YAML.sublime-syntax',
    '.profile': 'Packages/ShellScript/Bash.sublime-syntax',
    '.bashrc*': 'Packages/ShellScript/Bash.sublime-syntax',
    'bash': 'Packages/ShellScript/Bash.sublime-syntax',
    'sh': 'Packages/ShellScript/Bash.sublime-syntax',
    'zsh': 'Packages/ShellScript/Bash.sublime-syntax',
    '.helmignore': 'Packages/Git Formats/Git Ignore.sublime-syntax',
    '.dockerignore': 'Packages/Git Formats/Git Ignore.sublime-syntax',
    '**/templates/*.yml': 'Packages/Go/YAML (Go).sublime-syntax',
    '**/templates/*.yaml': 'Packages/Go/YAML (Go).sublime-syntax',
    '**/templates/*.tpl': 'Packages/Go/YAML (Go).sublime-syntax',
}


class SyntaxMapperListener(sublime_plugin.EventListener):
    """Simple Sublime Text plugin for mapping file extensions to syntax."""

    def on_load(self, view):
        self.apply_syntax(view)

    def on_post_save(self, view):
        self.apply_syntax(view)

    def apply_syntax(self, view):
        file_name = view.file_name()
        if not file_name:
            return

        base_name = os.path.basename(file_name)

        for pattern, syntax in PATTERNS.items():
            # If the pattern contains an asterisk, that's a glob. If the pattern
            # contains a slash, that's a glob for the full path. Otherwise,
            # that's the exact extension match.
            if '*' in pattern and '/' in pattern:
                if fnmatch(file_name, pattern):
                    self.set_syntax(view, syntax)
                    return
            elif '*' in pattern:
                if fnmatch(base_name, pattern):
                    self.set_syntax(view, syntax)
                    return
            else:
                # Check exact filename match
                if base_name == pattern:
                    self.set_syntax(view, syntax)
                    return

                # Check extension (without dot)
                _, ext = os.path.splitext(base_name)
                if ext and ext[1:] == pattern:
                    self.set_syntax(view, syntax)
                    return

                # Check compound extensions (e.g., yml.dist, html.erb)
                parts = base_name.split('.')
                if len(parts) > 2:
                    compound_ext = '.'.join(parts[-2:])
                    if compound_ext == pattern:
                        self.set_syntax(view, syntax)
                        return

    def set_syntax(self, view, syntax_name):
        # If full path is provided, use it directly
        if syntax_name.startswith('Packages/'):
            view.set_syntax_file(syntax_name)
            return

        # Otherwise try common syntax file locations
        syntax_paths = [
            'Packages/{0}/{0}.sublime-syntax'.format(syntax_name),
            'Packages/{0}/{0}.tmLanguage'.format(syntax_name),
        ]

        for syntax_path in syntax_paths:
            try:
                view.set_syntax_file(syntax_path)
                return
            except:
                continue
