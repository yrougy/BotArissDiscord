# Ariss Contact Discord Bot

This bot is making announces in a Discord Channel when an ARISS contact is scheduled during the next two weeks. 
It's a quick and dirty script, but it works.

- It get the events from an ICS calendar from the network
- In this configuration, it filter only European passes but can be easily converted to other regions

## Installation

I highly recommend you use a virtual-env to install it.

### Pre-requisites

You will need:
1. The Discord Channel ID to publish to.
    To find it, you need to turn your discord app in developer mode (From you **user** settings -> advanced -> Developer mode)
    Then right click on the channel you want the id, et you have the ability to copy it in the contextual menu
1. A Discord API key
    - Got to the Discord developper portal https://discord.com/developers/applications and connect your account
    - Go to **New Application** (top right)
    - Give a name to your bot
    - On the left menu choose **Bot**
    - Click on **Reset Token** and Copy and save your Token. It won't show again
    - In the **Privileged Gateway Intents** part of the page, check the **Message Content Intent** switch so the bot is allowed to send messages.

### Configuration of the script

At the begining of the script you have to
- Set the **DiscordChannel** id you want to publish to with the one you got on the previous step
- Set the **BotKEY** Discord API key with the Token you got in the previous step
- You can change the **Location** to your area. It's the one from the "FM over Europe" string in the event. Put "." if you want the whole world.

### Setup of the script

1. Create a `virtualenv` 
You may need to replace python with python3 on some platforms.
```
python -m venv arissenv 
source arissenv/bin/activate
```
2. You install the requirements
```
pip install -r requirements.txt
```

### Use of the script

I run this script each week with
```
. arissenv/bin/activate
python arissBotDiscord.py
```

