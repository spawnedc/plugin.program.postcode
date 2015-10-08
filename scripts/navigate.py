import subprocess

command = [
    'dbus-send',
    '--print-reply',
    '--session',
    '--dest=org.navit_project.navit',
    '/org/navit_project/navit/default_navit',
    'org.navit_project.navit.navit.set_destination',
    'string:"geo:-2.59247615 51.45423724" string:"BS12AW"'
]

subprocess.call(command)
