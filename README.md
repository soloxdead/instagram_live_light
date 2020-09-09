# Instagram Live Light Control
This application allows users during Instagram Live control your TP-Link light bulb. IG Live Light Control uses [Ping's Instagram_Private_Api](https://github.com/ping/instagram_private_api) and [Konsumer's tplink-lightbulb](https://github.com/konsumer/tplink-lightbulb). IGLLC is a modified version of Instagram_Private_Api callback login which can be [found here](https://github.com/ping/instagram_private_api/blob/master/examples/savesettings_logincallback.py)

## Instructions
1. Download and install Instagram_Private_Api
2. Download tplight.exe from tplink-lightbulb
3. Manually add your Instagram's Live Broadcast ID (instructions below) and TP-Link SmartBulb IP address to appropriate location.
4. Run instagram.py with the following command
```
python3 instagram.py -u ig_name -p ig_password -settings auth.json
```
* -settings auth.json saves auth_token to prevent getting banned from logging in too many times *

## Known Issues
1. The program crashes if there has not been any text written within 20-30 secs. It is programmed to look for text every 3 seconds. If nothing has been said in a short amount of time, the program triggers an error.
2. Not so much of an error but would like to grab the Live Broadcast ID automatically.
3. Program only works when 2-factor authentication is turned off. 

## Getting IG Live Broadcast ID
In order to get the Broadcast ID, you need to visit your live stream through a browser. View the source, and find the "broadcast_id".
