## Simple Interactive SteamCMD Wrapper for Python

Inspired by https://github.com/wmellema/Py-SteamCMD-Wrapper

### Purpose
Simple wrapper to make it easier to use SteamCMD with python. It tries to solve problem of downloading a lot of huge files (workshop mods), during which SteamCMD might timeout making it a headache to automatize.

### Usage example
```python
    # Creating instance
    steam = InteractiveSteamCMD("/home/steam/steamcmd")
    # Creating instance
    try:
        steam.install()
    except SteamCMDAlreadyInstalled:
        pass # already installed
    
    path = "/"
    with self.steam.run() as steam_cmd:
        # download arma 3 server
        steam_cmd.update_app(233780, path)
        # download mods for arma
        steam_cmd.update_workshop_mod(107410, 450814997, path)
```