# Haven't you wished you could "meme"-fy people at random?
## Table of Contents
<details><summary>Expand to see contents</summary>
  <p>

* **[Description](#Description)**<br />
* **[Motivation](#motivation)**<br />
* **[Getting Started](#getting-started)**<br />
* **[Deployment](#deployment)**<br />
* **[Author](#author)**<br />
* **[Contributing](#contributing)**<br />
* **[License](#license)**<br />

</p>
</details>

## Description
This project consists of a _python bot_ for telegram made to pick group chat messages of people that contain _"mentions"_ (basically any message where you type the **@username** of any member of a group chat), get the profile picture from the first mention on the message and then sticking up the text from the message the mention came from. The bot **does no** make this process for every single message with _"mentions"_. For every group, the bot will generate a **random number** and will wait for that amount of messages with mentions before making any image, after this the bot will generate a **new random number** and start again. This is done to avoid people constantly mentioning others and basically flooding group chats with replies from the bot. On the other hand, the bot could get annoying if every time anyone mentions another user for any reason, the bot sends a reply.

### Tools used
<details><summary>Expand to see contents</summary>
  <p>

* **Python v3.10.0+:** For the environment needed to code this bot.<br />
* **python-telegram-bot :** As the wrapper for the telegram API (you can fin it [here](https://github.com/python-telegram-bot/python-telegram-bot)).<br />
* **python-dotenv:** To load the .env file variables into the process enviroment (you can find it [here](https://github.com/theskumar/python-dotenv)).<br />
* **Pillow:** To manipulate images and add text to them (you can find it [here](https://github.com/python-pillow/Pillow)).<br />

</p>
</details>

## Motivation
A friend gave me the basic idea for this bot and since I personally haven't worked with editing images programatically before, I thought this would be a nice project to learn about such topic. If you would like to see the deployed version of this bot you can find it as @CaptionyBot on telegram or click [here](https://t.me/CaptionyBot). If you want to deploy it yourself, follow the instructions on the **[Getting Started](#getting-started)** section bellow.

## Getting Started
If you want to deploy this bot by yourself first you need to prepare a few things. First of all the bot needs at least 2 enviroment variables to work. Because one of the pyton modules used for the project allows you to create a `.env` file (basically a file with ".env" as it's name) I recommend you make such file on your environment to easily manipulate the variables you need. If you plan on deploying this bot on a cloud service like Heroku, please check how can you add environment variables to a project for the cloud service you will be using.

### Env Variables
Now, the env variables you need are the `ISPRODUCTION` variable (this tells the bot if it is deployed on a cloud environment like Heroku or not) please use `TRUE` or `FALSE` as the values for this variable. The port you want the webserver to run in a variable called `PORT` (This is an optional variable and I recommend using `8443` as the value for this variable if you are deploying on a cloud service like Heroku, if you are deploying on your own machine, just don't add this variable to your file) and an api token telegram will give you for your bot. Before you go for the api key remember the name of the env variable is `TELEGRAM_API`.

### Telegram Api Key
On telegram search for `@BotFather` and talk to him. type `/help` if you don't know what to do. Here you can make your bot, he will ask you for some information for the bot and then it will give you the Api key. If you want to give your bot a description, image, etc. Then here you can also do that.

### Clone or Download this repo
Now is when you clone/download this repo, make a folder for it and save it anywhere you want it to be, if you already made the .env file then save it in the same folder where the `src/` folder of this repo is (or create said file in such a place).

### Make sure you have python 
Before you begin make sure you have python and pip installed in your sistem. You can do it by typing:

```Powershell
python -V
pip -V
```
Those two commands should print you the versión of those programs you have installed. If you don't see any message or an error, then make sure you install [Python](https://www.python.org/) on your system.

### (Optional) Virtual Environment
If you want to separate this python project packages from other projects you might have, you can use a `venv` (Virtual Environment) for this project. To do this, **before you install any packages** you need to run this command:
```Powershell
python -m venv path/to/your/venv
```
I recomend you use ".venv/" for your path but you can use any other name you want. Just make sure you add it to your `.gitIgnore` file before pushing any changes to this repository. Once the environment is created, make sure to activate based on your OS/Terminal:
#### CMD
```
./path/to/your/venv/Scripts/Activate.bat
```
#### Powershell
```Powershell
./path/to/your/venv/Scripts/Activate.ps1
```
#### Bash or Zsh
```Sh
source bin/activate
```

### Install Modules
It is recommended you create a virtual enviorenment before installing any modules for the project, but it's completelly optional and up to you. Now, we are almost done, last thing we have to do before deployment is to add the required python modules, to do that you need to open a console in the path where you cloned/downloaded the repo and type:
```Powershell
pip install -r requirements.txt
``` 
pip will download and install all the modules required for the project. This can take a few seconds, but after it you are ready to deploy.

If you are deplying on a cloud envirenment like Heroku, check if the service you are using automatically performs this process or if you need to install thing manually.

## Deployment
### Deploy on your own machine
Now to deploy, please **remember to add the env variables to your console or operative system** if you didn't create a .env file. Now that everything is done open the console where you have this project and type:
```
python src/
```
when you see a message saying `The bot is up! :)` then it means the bot is active on telegram and ready to use.

### Deploy to cloud
If you are using a cloud environment to deploy this project, **please make sure you have all the env variables for the project configured before deploying**, you will need an extra variable I haven't mentioned called `URL`, this variable needs to hold the url of your project, if you do so, the bot will connect to the Telegram api using webhooks instead of long polling, which can help improve performance and also makes sure the bot won't fall "asleep" on certain cloud services after some time. After that, you just need to push the contents of this repo to your cloud service and everything should be good to go.

### Deploy on other cloud services
I have only worked with heroku for deploying bots, that's why I can't tell you how to deploy on other cloud services. Python-telegram-bot does have **[guides on how to do this process](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot)**, but you might have to edit some of the code and files from this repo before trying this.

## Authors
* [__Camilo Zambrano Votto__](https://github.com/cawolfkreo)

## Contributing
If anyone wants to give me any help or ideas, you can by making new [Issues](https://github.com/cawolfkreo/Caption-Users-Picures-Bot/issues) or [Pull requests](https://github.com/cawolfkreo/Caption-Users-Picures-Bot/pulls).

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository has the standard MIT license. You can find it [here.](https://github.com/cawolfkreo/Caption-Users-Picures-Bot/blob/master/LICENSE)