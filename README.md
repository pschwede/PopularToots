# Popular toots

A bot that toots about the most retweeted and most faved local toot.

## Setup

Run `create.py` to setup the account that will act as this bot.

Run `virtualenv -p python3 .` to create a local environment that will be activated by `run.sh`.

Add `run.sh` to your `crontab -e`, for example:

```
0	22	*	*	*	/your/path_to/populartoots/run.sh
```
