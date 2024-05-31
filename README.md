## Py-SteamCMD-Subprocess-Wrapper

### Purpose
Simple wrapper to make it easier to use SteamCMD with python.

The idea came when I tried to install 100+ mods to Arma 3. Those mods varied in size from 2 KB to +20 GB.
To automate this I tried using other automation libraries, but they didn't solve the problem as they were simply
invoking.
```bash
./steamcmd.sh +login {username} {password} {2fa} +workshop_download_item 107410 450814997 +quit
```
multiple times which could lead to timeouts due to 2FA rate limiting.
Which created need of persistent client.

## Notes
- Disabling 2FA only moves the problem further as without 2FA you get the code on your e-mail
which makes it even harder to automate
- Some games (Arma 3 included) and their server require logged user to own the original game, so we cannot login
as anonymous
- Custom script for SteamCMD looks good on paper however you have to keep in mind that SteamCMD is bad. It can randomly timeout
while downloading mods (especially if they are big in size). If SteamCMD fails in the middle of the script you would
need to manually amend the script or risk running it again unchanged, which would validate all apps/mods again risking 
yet another timeout.
- Originally I used it to run it on Jenkins Pipeline to keep mods updates on my machine.


### Dependencies
You need to be able to manually run SteamCMD on your OS.

For Debian-Based Distributions (Ubuntu, Mint, etc.) this should be enough:
```shell
apt-get install lib32gcc1  # Debian
```
for details visit official docs:
[SteamCMD docs Known Issues](https://developer.valvesoftware.com/wiki/SteamCMD#ERROR.21_Failed_to_install_app_.22xxxxxx.22_.28No_subscription.29)


### Usage example

```python
from steamcmd_wrapper import get_steamcmd_client

client = get_steamcmd_client("//Steam")

client.set_install_dir("/steamcmd")  # SteamCMD official docs recommend setting dir before login 
client.login_as_anonymous()  # or client.login(user, password) if you need to own the game

client.update_app("app_id")
client.update_workshop_mod("app_id", "mod_id")
```
