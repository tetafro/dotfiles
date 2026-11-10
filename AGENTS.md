# Repository guidance

- This repo is the source of truth for configs installed through symlinks and
  hard links. Trace their destinations in `install.sh` and `work/install.sh`.
- Edit the source files here. Changes to linked files can affect the live
  environment immediately; replacing a hard-linked file can break the link.
- For configs you are working on, check that live destinations still link to
  the repo sources: verify symlink targets or shared inodes for hard links.
  External tools can replace live files and break these links. Limit this check
  to configs involved in the task.
- `home/` contains personal configs and scripts; `work/` contains local work
  configs and is ignored except for `.gitkeep`. Keep work-only content untracked.
- Run installers from the repo root only when explicitly requested: they replace
  live configs, remove directories, and load GNOME Terminal settings.
- Keep changes small and consistent with nearby files. Validate changed shell
  scripts with `bash -n`; do not source them just to check syntax.
