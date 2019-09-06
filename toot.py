#!/usr/bin/env python3

import re
from os import path
from config import APIBASE, USERSECRET
from mastodon import Mastodon


TWITTERNAME = re.compile(r'(@[a-zA-Z0-9@-_]+)')


def post_mastodon(message="#test"):
    if not path.exists(USERSECRET):
        return 1
    mastodon = Mastodon(
            access_token = USERSECRET,
            api_base_url = APIBASE
            )

    try:
        mastodon.toot(message)
    except Exception as e:
        print("Toot failed: %s" % e)


if __name__ == "__main__":
    import sys

    for line in sys.stdin:
        post_mastodon(message=line)
