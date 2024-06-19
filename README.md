# dot

Yet another dotfiles repo! Files are organized by hostname and maintained by [update.sh](./update.sh)

A _relatively_ recent Linux desktop is assumed throughout; PRs are always welcome!
_I use Fedora btw :)_

## Notable entries

### i3/Sway auto-start script

Time/date aware autostart manager. The script: [.config/sway/scripts/startup.py](./outerheaven.init3.home/.config/sway/scripts/startup.py)

This reads [.config/autostart-i3ipc.yml](./outerheaven.init3.home/.config/autostart-i3ipc.yml)
to know what programs to `exec`. Example:

```yaml
---
autostarts:
  pre:        # *always* run, before/blocking others. ie: backup
  weekend: [] # blocking Sat/Sun. after 'pre'/before 'common'. ie: backup tier 2
  common: []  # things started every day, after 'pre' - non-blocking
  work: []    # does not execute on weekends; only if within working day/hours
```
Touch `~/.vacation` to skip `work` autostarts; remove the file when work may begin again :)

Working days are assumed Monday through Friday. Hours are between 8 AM and 4 PM.
These parameters may be changed in the `WorkTime` class.
