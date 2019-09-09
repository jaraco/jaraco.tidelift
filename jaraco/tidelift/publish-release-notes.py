import os
import sys
import subprocess

import autocommand
from requests_toolbelt import sessions


url = 'https://api.tidelift.com/external-api/'
session = sessions.BaseUrlSession(url)
session.headers = dict(Authorization=f'Bearer {os.environ.get("TIDELIFT_TOKEN")}')


@autocommand.autocommand(__name__)
def run(template='https://{flat_name}.readthedocs.io/en/latest/history.html'):
    name, version = subprocess.run(
        [sys.executable, 'setup.py', '--name', '--version'],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.split()
    platform = 'pypi'
    path = f'lifting/{platform}/{name}/release-notes/{version}'
    data = template.format(
        flat_name=name.replace('.', ''),
        flat_ver=version.replace('.', ''),
        **locals()
    )
    session.post(path, data=data).raise_for_status()
