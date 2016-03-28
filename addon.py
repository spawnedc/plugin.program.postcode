import xbmcgui
import xbmcaddon
import re
import sqlite3
import os
import dbus

addon = xbmcaddon.Addon(id="plugin.program.postcode")

__addonname__ = addon.getAddonInfo('name')
__addonpath__ = addon.getAddonInfo('path')

resources_path = os.path.join(__addonpath__, 'resources')
scripts_path = os.path.join(__addonpath__, 'scripts')

sqlite_file = os.path.join(resources_path, 'pc_lat_lon_gb.sqlite')


def fix_postcode(postcode):
    return postcode.upper().replace(' ', '')


def postcode_to_latlng(postcode):
    latlng = None

    conn = sqlite3.connect(sqlite_file)
    cur = conn.cursor()
    sql = "SELECT lat,lng FROM lat_lon_gb WHERE postcode='%s'" % postcode
    cur.execute(sql)
    row = cur.fetchone()
    latlng = ','.join([row[0], row[1]])
    cur.close()

    return latlng


def validate_postcode(postcode=''):
    pattern = r'^[A-Z]{1,2}[0-9R][0-9A-Z]?[0-9][ABD-HJLNP-UW-Z]{2}$'
    results = re.findall(pattern, postcode)

    if len(results):
        return True

    return False


def navit_dbus(lng, lat, title=''):
    command = "RunScript(%s/navigate.py, %s, %s, %s)" % (scripts_path, lng, lat, title)
    xbmc.log(command)
    xbmc.executebuiltin(command)

postcode = fix_postcode(xbmcgui.Dialog().input('Enter a postcode'))
valid_postcode = validate_postcode(postcode)

if valid_postcode:
    pDialog = xbmcgui.DialogProgress()
    pDialog.create(__addonname__, 'Searching for postcode...')
    latlng = postcode_to_latlng(postcode)
    pDialog.close()

    (lat, lng) = latlng.split(',')
    navit_dbus(lng, lat, postcode)

    xbmc.executebuiltin('RunScript("plugin.program.navigation")')
else:
    xbmcgui.Dialog().ok(__addonname__, 'Not a valid postcode')
