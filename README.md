# Popular toots

A bot that toots about the most retweeted and most faved local toot.

## Setup

Run `python3 -m venv .env` to create a local, independent environment that will later be activated by `run-daily.sh`, etc.

Run to install all requirements:
```bash
source .env/bin/activate
pip install -r requirements.txt
deactivate
```

Run `create.py` to setup the account that will act as this bot.

Add `run-daily.sh` and `run-hourly.sh` to your `crontab -e`, for example:

```
0	22	*	*	*	/your/path_to/populartoots/run-daily.sh
@hourly					/your/path_to/populartoots/run-hourly.sh
```
