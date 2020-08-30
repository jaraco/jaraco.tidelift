import os
import sys
import subprocess
import getpass

import keyring
import autocommand
from requests_toolbelt import sessions


session = sessions.BaseUrlSession('https://api.tidelift.com/external-api/')


def load_token():
    token = os.environ.get("TIDELIFT_TOKEN") or keyring.get_password(
        'https://api.tidelift.com/external-api/', getpass.getuser()
    )
    assert token, "Token not available"
    return token


@autocommand.autocommand(__name__)
def run(template='https://{flat_name}.readthedocs.io/en/latest/history.html'):
    session.headers.update(Authorization=f'Bearer {load_token()}')
    name, version = subprocess.run(
        [sys.executable, 'setup.py', '--name', '--version'],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.split()
    platform = 'pypi'
    path = f'lifting/{platform}/{name}/release-notes/{version}'
    data = template.format(
        flat_name=name.replace('.', ''), flat_ver=version.replace('.', ''), **locals()
    )
    session.post(path, data=data).raise_for_status()
