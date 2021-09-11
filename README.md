# PyCon TW Registration Bot

## Description
This bot is developed for registration users on Discord Server during PyCon TW 2021.
In the direct message channel to RegBot, users can register themselves by sending `!register <TOKEN>`.
User can use his/her own token to get the role he/she should get.

## Commands list
* `!register <TOKEN>`: Register yourself with given token
* `!help`: Shows the help message
* `!help <COMMAND>`: Shows description of each command
* `!hello <MESSAGE>`: Just say hello to bot.
* `!howto`: Show instruction about how to register

## Tokens
Tokens should be stored under "tokens" folder. Because ticket has different type, there are three different csv files: "corporate.csv", "individual.csv", "reserved.csv" to represent different ticket type.

## Log
The log file is stored under ".log" folder and saved as "reg.log".