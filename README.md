# PyCon TW Registration Bot

## Description
This bot is developed for registration users on Discord Server during PyCon TW 2021.
In the direct message channel to RegBot, users can register themselves by sending `!register <TOKEN>`.
User can use his/her own token to get the role he/she should get.

## Development environment

### Prerequisite

| Name | Version |
| --- | --- |
| Python | 3.8 |
| pipenv(Python module) | 2021.5.29 or up |

### Environment setup

0. Initialize environment variable

```
cp sample.env .env
```
1. Initialize Python environment

```
pipenv install --dev
```

2. Enter the environment and start developing

```
pipenv shell
```

3. Run bot and give it a try

```
python3 bot.py
```

### QRcode Tokens

#### How to Get Tokens for `corporate.csv` and `individual.csv`?

```sql
SELECT
  REPLACE(JSON_EXTRACT(ATTENDEE_INFO, '$.qrcode'), '"', '') AS token
FROM
  `pycontw-225217.ods.ods_kktix_attendeeId_datetime`
WHERE
  (REFUNDED IS NULL
    OR REFUNDED = FALSE)
  AND NAME LIKE '%<year>%'  -- year param: 20xx of course
  AND LOWER(NAME) LIKE '%<type>%';  -- type param: <corporate, individual>
#### Where to Put These Tokens

Tokens should be stored under "tokens" folder.

Because ticket has different types, there are three different CSV files
to represent each ticket type:
* `corporate.csv` for corporate tickets
* `individual.csv` for individual tickets
* `reserved.csv` for reserved tickets

Each token is stored with the following format:
```
d41d8cd98f00b204e9800998ecf8427e,<ticket_type>
```

Redeemed tokens will be stored in `used.csv` with the following format:
```
d41d8cd98f00b204e9800998ecf8427e
```

### Logging
The log file is stored under `.log` folder and saved as `reg.log`.

## Usage

### Commands list
* `!register <TOKEN>`: Register yourself with given token
* `!help`: Shows the help message
* `!help <COMMAND>`: Shows description of each command
* `!hello <MESSAGE>`: Just say hello to bot.
* `!howto`: Show instruction about how to register
