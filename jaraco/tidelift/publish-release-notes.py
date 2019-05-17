import os
import sys
import subprocess

import autocommand
from requests_toolbelt import sessions


url = 'https://api.tidelift.com/external-api/'
session = sessions.BaseUrlSession(url)
session.headers = dict(Authorization=f'Bearer {os.environ.get("TIDELIFT_TOKEN")}')


@autocommand.autocommand(__name__)
def run():
    name, version = subprocess.run(
        [sys.executable, 'setup.py', '--name', '--version'],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.split()
    platform = 'pypi'
    path = f'lifting/{platform}/{name}/release-notes/{version}'
    rtd_name = name.replace('.', '')
    release_notes = f'https://{rtd_name}.readthedocs.io/en/latest/history.html'
    session.post(path, data=release_notes).raise_for_status()
