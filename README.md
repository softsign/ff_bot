Shoutout to /u/rbart65 on reddit and rbarton65 on github for creating the original version of the chatbot and the ESPN FF API.

Further shoutouts to **dtcarls** for building the GroupMe bot, and to **uberfastman** for building fantasy-football-metrics, which helped lay the groundwork for this.

This is a major work in progress, but it works as-is. YMMV. I'm a Python newbie, so very open to suggestions on improving things. 

I have not tested the Docker stuff, and have not tested Slack, though it should be close to working as-is. 

For now, I only know that this works in a Python 3 virtualenv. To make it work, register your app with Yahoo and add the consumer key and secret to authentication/private.txt (see the sample). Next, set up your virtualenv, and run 'python first_time_token.py' (this is only necessary the first time, to get your OAuth tokens). Finally, set your league environment variables ('BOT_ID', 'LEAGUE_ID', 'YEAR') and execute 'python ff_bot.py'. I plan to streamline this eventually.

To get the callback bot working, make sure you have gunicorn installed (pip install gunicorn) and execute 'gunicorn -w 4 callbackbot:app -b [server]:[port]'.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# Yahoo Fantasy Football GroupMe Bot

This package creates a docker container that runs a GroupMe or Slack chat bot to send
Yahoo Fantasy Football information to a GroupMe or Slack chat room.

**What does this do?**

- Sends out the following messages on this schedule:
- Power rankings - tue -18:30
- Matchups - thu - 19:30 (Just upcoming matchups)
- Close Scores - mon - 18:30 (Games that are within 16 points of eachother to keep an eye on during the Monday night game)
- Trophies- tue - 7:30 (High score, low score, biggest win, closest win)
- Scoreboard - fri,mon,tue - 7:30 (Current Yahoo fantasy scoreboard)
- Scoreboard - sun - 16:30, 20:30 (Current Yahoo fantasy scoreboard)

## Getting Started

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.

### Installing
With Docker:
```bash
git clone https://github.com/softsign/yahoo_ff_bot

cd ff_bot

docker build -t ff_bot .
```

Without Docker:

```bash
git clone https://github.com/softsign/yahoo_ff_bot

cd yahoo_ff_bot

python3 setup.py install
```


## Basic Usage

This gives an overview of all the features of `yahoo_ff_bot`

### Environment Variables

- BOT_ID: This is your Bot ID from the GroupMe developers page (REQUIRED IF USING GROUPME)
- WEBHOOK_URL: This is your Webhook URL from the Slack App page (REQUIRED IF USING SLACK)
- LEAGUE_ID: This is your Yahoo league id (REQUIRED)
- START_DATE: This is when the bot will start paying attention and sending messages to GroupMe or Slack. (2018-09-05 by default)
- END_DATE: This is when the bot will stop paying attention and stop sending messages to GroupMe or Slack. (2018-12-26 by default)
- LEAGUE_YEAR: Yahoo League year to look at (2018 by default)
- TIMEZONE: The timezone that the messages will look to send in. (America/New_York by default)
- INIT_MSG: The message that the bot will say when it is started (“Hai” by default, can be blank for no message)

### Running with Docker

Use BOT_ID if using Groupme, and WEBHOOK_URL if using Slack (or both to get messages in both places)

```bash
>>> export BOT_ID=[enter your GroupMe Bot ID]
>>> export WEBHOOK_URL=[enter your Webhook URL]
>>> export LEAGUE_ID=[enter Yahoo league ID]
>>> export LEAGUE_YEAR=[enter league year]
>>> cd ff_bot
>>> docker run --rm=True \
-e BOT_ID=$BOT_ID \
-e LEAGUE_ID=$LEAGUE_ID \
-e LEAGUE_YEAR=$LEAGUE_YEAR \
ff_bot
```

### Running without Docker

Use BOT_ID if using Groupme, and WEBHOOK_URL if using Slack (or both to get messages in both places)

```bash
>>> export BOT_ID=[enter your GroupMe Bot ID]
>>> export WEBHOOK_URL=[enter your Webhook URL]
>>> export LEAGUE_ID=[enter Yahoo league ID]
>>> export LEAGUE_YEAR=[enter league year]
>>> cd ff_bot
>>> python3 ff_bot.py
```

## Setting up GroupMe or Slack, and deploying app in Heroku

**Do not deploy 2 of the same bot in the same chat. In general, you should let your commissioner do the setup**

### GroupMe Setup

Go to www.groupme.com and sign up or login

If you don't have one for your league already, create a new "Group Chat"

![](https://i.imgur.com/32ioDoZ.png)

Next we will setup the bot for GroupMe

Go to https://dev.groupme.com/session/new and login

Click "Create Bot"

![](https://i.imgur.com/TI1bpwE.png)

Create your bot. GroupMe does a good job explaining what each thing is.

![](https://i.imgur.com/DQUcuuI.png)

**If you plan to run the callback bot, DO SPECIFY THE URL.**
 
After you have created your bot you will see something similar to this. Click "Edit"

![](https://i.imgur.com/Z9vwKKt.png)

This page is important as you will need the "Bot ID" on this page.You can also send a test message with the text box to be sure it is connected to your chat room.
Side note: If you use the bot id depicted in the page you will spam an empty chat room so not worth the effort

![](https://i.imgur.com/k65EZFJ.png)

### Slack setup

Go to https://slack.com/signin and sign in to the workspace the bot will be in

If you don't have one for your league already, create a new League Channel

Next we will setup the bot for Slack

Go to https://api.slack.com/apps/new

Name the app, and choose the intended workspace from the dropdown.

Select the Incoming Webhooks section on the side.

![](https://i.imgur.com/ziRQCVP.png)

Change the toggle from Off to On.

Select Add New Webhook to Workspace

![](https://i.imgur.com/tJRRrfz.png)

In the Post to dropdown, select the channel you want to send messages to, then
select Authorize.

This page is important as you will need the "Webhook URL" on this page.

![](https://i.imgur.com/mmzhDS0.png)

### Heroku setup

Heroku is what we will be using to host the chat bot (for free)

**You should not need to enter credit card information for this hosting service for our needs.**
You **may** run out of free hours without a credit card linked. If you decide to link your credit card you will have enough free hours for the month for a single application since this more than doubles your available hours. We are not responsible for any charges associated with Heroku.

Go to https://id.heroku.com/login and sign up or login


**!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

**Click this handy button:**
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

**!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

Go to your dashboard (https://dashboard.heroku.com/apps)
Now you will need to setup your environment variables so that it works for your league. Click Settings at your dashboard. Then click "Reveal Config Vars" button and you will see something like this.

![](https://i.imgur.com/7a1V6v8.png)

Now we will need to edit these variables (click the pencil to the right of the variable to modify)
Note: App will restart when you change any variable so your chat room may be semi-spammed with the init message of "Hai" you can change the INIT_MSG variable to be blank to have no init message. It should also be noted that Heroku seems to restart the app about once a day

- BOT_ID: This is your Bot ID from the GroupMe developers page (REQUIRED IF USING GROUPME)
- WEBHOOK_URL: This is your Webhook URL from the Slack App page (REQUIRED IF USING SLACK)
- LEAGUE_ID: This is your Yahoo league id (REQUIRED)
- START_DATE: This is when the bot will start paying attention and sending messages to GroupMe or Slack. (2018-09-05 by default)
- END_DATE: This is when the bot will stop paying attention and stop sending messages to GroupMe or Slack. (2018-12-26 by default)
- LEAGUE_YEAR: Yahoo League year to look at (2018 by default)
- TIMEZONE: The timezone that the messages will look to send in. (America/New_York by default)
- INIT_MSG: The message that the bot will say when it is started (“Hai” by default, can be blank for no message)

After you have setup your variables you will need to turn it on. Navigate to the "Resources" tab of your Heroku app Dashboard.
You should see something like below. Click the pencil on the right and toggle the buton so it is blue like depicted and click "Confirm."
![](https://i.imgur.com/J6bpV2I.png)

You're done! You now have a fully featured GroupMe/Slack chat bot for Yahoo leagues! If you have an INIT_MSG you will see it exclaimed in your GroupMe or Slack chat room.

Unfortunately to do auto deploys of the latest version you need admin access to the repository on git. You can check for updates on the github page (https://github.com/softsign/yahoo_ff_bot/commits/master) and click the deploy button again; however, this will deploy a new instance and the variables will need to be edited again.
