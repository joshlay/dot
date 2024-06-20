# dot

Yet another dotfiles repo! Files are organized by hostname and maintained by [update.sh](./update.sh)

A _relatively_ recent Linux desktop is assumed throughout; PRs are always welcome!
_I use Fedora btw :)_

## Notable entries

### i3/Sway auto-start script

<details>
  <summary><i>Click to expand...</i></summary>
  
  Time/date aware autostart manager. The script: [.config/sway/scripts/startup.py](./outerheaven.init3.home/.config/sway/scripts/startup.py)
  
  This is run by Sway on-login:
  
  ```bash
  ~ $ cat ~/.config/sway/config
  # Config for sway
  #
  # See `man 5 sway` for a complete reference.
  # [...]
  # run script which handles conditional/timely autostarts. uses dict w/ this structure:
  # {'autostarts': { 'pre': [], 'weekend': [], 'common': [], 'work': []}}
  exec 'python3 ~/.config/sway/scripts/startup.py'
  ```
  
  This reads [autostart-i3ipc.yml](./outerheaven.init3.home/.config/autostart-i3ipc.yml)
  _(in `~/.config`)_ to know what programs to `exec`.
  
  Example with in-line comments:
  
  ```yaml
  ---
  autostarts:
    pre: []     # *always* run, before/blocking others. ie: backup
    weekend: [] # blocking Sat/Sun. after 'pre'/before 'common'. ie: backup tier 2
    common: []  # things started every day, after 'pre' - non-blocking
    work: []    # does not execute on weekends; only if within working day/hours
  ```
  
  Touch `~/.vacation` to skip `work` autostarts; `rm` when work may continue :)
  
  Working days are assumed Monday through Friday. Hours are between 8 AM and 4 PM.
  These parameters may be changed in the `WorkTime` class.

</details>

### homedir backup script

<details>
  <summary><i>Click to expand...</i></summary>

  Intended as part of the auto-starts above, I have [written a script](./outerheaven.init3.home/.local/bin/backup_home)
  to back up `$HOME`  
  _(minus exclusions, of course)!_

  The meaningful work is given away to other utilities:

* `restic`: performs the backup
* `pass`: stores the passphrase given to `restic`; prompts for confirmation on hardware token

</details>
