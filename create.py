#!/usr/bin/env python3

from os import path
from config import SECRETFILE, APPNAME, APIBASE, USERSECRET
from getpass import getpass
from mastodon import Mastodon

if path.exists(SECRETFILE):
    print("Secret file already exists: %s" % SECRETFILE)
else:
    Mastodon.create_app(
            APPNAME,
            api_base_url = APIBASE,
            to_file = SECRETFILE
            )
mastodon = Mastodon(
        client_id = SECRETFILE,
        api_base_url = APIBASE
        )
mastodon.log_in(
        input("Account (email) for %s: " % APIBASE),
        getpass("Mastodon password: "),
        to_file = USERSECRET
        )
