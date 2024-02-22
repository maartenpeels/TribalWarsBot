# TribalWarsBot

## Description

This is a bot for the game Tribal Wars. It is written in Python and uses web requests to interact with the game.

## Installation

1. Install python `3.11` or set up a virtual environment with python
2. Clone the repository
3. Install the required packages with `python -m pip install -r requirements.txt`
4. Run the bot with `python main.py`

## Usage

The first time it will ask some questions to set up the configuration.

## Configuration

### Version

This is the version of the configuration file. It is used to check if the configuration file should be updated based on
the new example config.

### Bot

#### log_level

The log level of the bot. It can be one of the following: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

#### auto_manage_new_villages

If this is set to `true` the bot will automatically manage new villages. If it is set to `false` the bot will ask to
manage new villages.

#### delays

##### request

The minimum and maximum delay after a request in seconds (can be floats).

### village_template

This is the template for used for villages.

#### id

The village id.

#### name

The village name.

#### manage

Is this village managed by the bot.

### web

#### server

Server that is used. Can be found in the url of the game.

#### domain

Domain that is used. Can be found in the url of the game.

#### user-agent

The user agent that is used for the web requests. It is important to use the user agent of your browser to avoid being
banned.

### villages

List of villages that are managed by the bot. This has the same format as the `village_template`.
