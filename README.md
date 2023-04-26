## Simple Interactive SteamCMD Wrapper for Python

Inspired by https://github.com/wmellema/Py-SteamCMD-Wrapper

### Purpose
Simple wrapper to make it easier to use SteamCMD with python. It tries to solve problem of downloading a lot of huge files (workshop mods), during which SteamCMD might timeout making it a headache to automatize.
Also using standard approach of multiple invocation of
```bash
./steamcmd.sh +login username password 2fa +workshop_download_item 107410 450814997 +quit
```
may cause Rate Limit Exceed Error due to trying to login with 2FA too quickly, wich current approach also solves.

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
        # some mods require account with a bought game
        steam_cmd.login(login, password, 2fa)
        # steam_cmd.login()  # to login as anonymous
        # download arma 3 server
        steam_cmd.update_app(233780, path)
        # download mods for arma
        steam_cmd.update_workshop_mod(107410, 450814997, path)
```

It's not 100% fool proof if SteamCMD subproccess closes unexpectedly or it returns some unexpected value. The script might fail.
