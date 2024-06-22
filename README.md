# dot

Yet another dotfiles repo! Files are organized by hostname and maintained by [update.sh](./update.sh)

A _relatively_ recent Linux desktop is assumed throughout; PRs are always welcome!
_I use Fedora btw :)_

## Quick Links

`.config`/system:

* [workstation](./outerheaven.init3.home/.config)

## Notable entries

### i3/Sway autostarts

_Script:_ [~/.config/sway/scripts/startup.py](./outerheaven.init3.home/.config/sway/scripts/startup.py)  
_Config:_ [~/.config/autostart-i3ipc.yml](./outerheaven.init3.home/.config/autostart-i3ipc.yml)

Time/date aware _(conditional)_ autostart manager for Sway/i3 window managers.

Should run on-login -- `i3`/`sway` having a config entry:

```bash
~ $ cat ~/.config/sway/config
# Config for sway
#
# See `man 5 sway` for a complete reference.
# [...]
exec 'python3 ~/.config/sway/scripts/startup.py'
```

Use `exec` as shown; avoid `exec_always`. Your _'wanted'_
entries will repeat, otherwise, if reloading i3/Sway.

Example `autostart-i3ipc.yml`:

```yaml
---
autostarts:
  pre: []     # *always* run, before/blocking others. ie: backup
  weekend: [] # blocking Sat/Sun. after 'pre'/before 'common'. ie: backup tier 2
  common:     # things started every day, after 'pre' - non-blocking
    - 'firefox-wayland'
    - 'foot'
  work: []    # does not execute on weekends; only if within working day/hours
```

Touch `~/.vacation` to skip `work` autostarts; `rm` when work may continue :)

Working days are assumed Monday through Friday. Hours are between 8 AM and 4 PM.
Defined in the `WorkTime` class.

***

### homedir backup

_Script:_ [~/.local/bin/backup_home](./outerheaven.init3.home/.local/bin/backup_home)  
_Config:_ `~/.restic_excludes`

This will back up `$HOME` _(minus exclusions, of course!)_. Part of
[the autostarts](#i3sway-autostarts).

The important parts are managed by others:

* `restic`: performs the backup to `$BACKUP_DEST` or `/raid1-evos/backups/restic`
_(if unset)_
* `pass`: stores the passphrase given to `restic`; confirmation on hardware token

The exclusions are highly personalized, and as such, _not_ included.
Wants _shell patterns_ split by lines.
