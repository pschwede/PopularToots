# Popular toots

A bot that toots about the most retweeted and most faved local toot.

## Setup

Run `python3 -m venv .env` to create a local environment that will be activated by `run*.sh`.

Run `create.py` to setup the account that will act as this bot.

Add `run-daily.sh` and `run-hourly.sh` to your `crontab -e`, for example:

```
0	22	*	*	*	/your/path_to/populartoots/run-daily.sh
@hourly					/your/path_to/populartoots/run-hourly.sh
```
