import json
import codecs
import datetime
import os
import os.path
import logging
import argparse
import time
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version, ClientCompatPatch)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='login callback and save settings demo')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(client_version))

    device_id = None
    try:

        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print('Unable to find file: {0!s}'.format(settings_file))

            # login new
            api = Client(
                args.username, args.password,
                on_login=lambda x: onlogin_callback(x, args.settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                args.username, args.password,
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username, args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.auth_expires
    print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))
    color_chart = {'lightsalmon': 'FFA07A', 'salmon': 'FA8072', 'darksalmon': 'E9967A', 'lightcoral': 'F08080', 'indianred': 'CD5C5C', 'crimson': 'DC143C', 'firebrick': 'B22222', 'red': 'FF0000', 'darkred': '8B0000', 'coral': 'FF7F50', 'tomato': 'FF6347', 'orangered': 'FF4500', 'gold': 'FFD700', 'orange': 'FFA500', 'darkorange': 'FF8C00', 'lightyellow': 'FFFFE0', 'lemonchiffon': 'FFFACD', 'lightgoldenrodyellow': 'FAFAD2', 'yellow': 'FFFF00', 'limegreen': '32CD32', 'lime': '00FF00', 'forestgreen': '228B22', 'green': '008000', 'darkgreen':  '006400', 'olive': '808000', 'cyan': '00FFFF', 'aqua': '00FFFF', 'aquamarine': '7FFFD4', 'turquoise':'40E0D0', 'teal': '008080', 'skyblue': '87CEEB', 'royalblue': '4169E1', 'blue': '0000FF', 'navy': '000080', 'lavender': 'E6E6FA', 'plum': 'DDA0DD', 'violet': 'EE82EE', 'fuchsia': 'FF00FF', 'magenta': 'FF00FF', 'purple': '800080', 'indigo': '4B0082', 'pink': 'FFC0CB', 'lightpink': 'FFB6C1','hotpink': 'FF69B4', 'white': 'FFFFFF', 'snow': 'FFFAFA', 'aliceblue': 'F0F8FF', 'silver': 'C0C0C0', 'gray': '808080', 'black': '000000', 'brown': 'A52A2A', 'maroon': '800000'}

    light_color = 'F0F8FF'
    while True:

        # Call the api
        results = api.feed_timeline()


        chat = api.broadcast_comments(broadcast_id='', last_comment_ts=0)
        
        color = chat['comments'][0]['text']
        color = color.lower()
        
        if color in color_chart:
            light_color = color_chart[color]
        else:
            light_color = light_color
        print(light_color)

        #Edit replace 'light_ip_address' with lights IP address
        os.system('./tplight hex light_ip_address ' + light_color)
        time.sleep(3)
