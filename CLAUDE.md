# Tomakuro

It's a minimalist Telegram tomato clock bot. The goal of this project is to provide users a useful tomato clock application that you can call immediately, whenever you want.

## Tech Stack

- **Package Management**: uv
- **Telegram Bot SDK**: python-telegram-bot


## Development Commands

In this project, I will give you the maximum permission to do whatever you want. I believe the only third-party library we need is python-telegram-bot. You need to install it and rebuild the entire application from scratch.

The functionality of this application is very simple. The ultimate goal of this application is to minimize the friction between the user and the usage of the application.

The only requirement is just a simple menu shown on the board. You don't need to add any commands by default. You don't need to show the text input bar; just show the menu on the menu board.

Here are the models you need to provide to users:

## Functionalities

### Start a tomato clock

When the user starts the bot, we will show a menu with three buttons:
1. The clock button
   After clicking the clock button, we will show another menu (the new menu). In the new menu, there are some fixed flight numbers:

    - 15 minutes
    - 30 minutes
    - 45 minutes
    - 60 minutes

    We can also add 90 minutes or 120 minutes. After clicking one of the numbers, we will start the tomato clock immediately and send a message to the user telling them the tomato clock is running.
2. The current status button: After the user clicks this button, the bot will send the basic information about the current tomato clock instance, such as:
   - When the tomato clock started
   - The estimated finish time
   - How long it has been running
  
   The menu will refresh with three buttons:
   1. Add some time
   2. Cancel this clock
   3. Return to the main menu
3. The stop button: After clicking the stop button, we will stop the current tomato clock immediately.

In this project, we usually use the innate user session management tools. I don't know the exact name, but you should try to find them in the documentation and use them. For each user using this tomato clock, it should have its own session management. I believe in the python-telegram-bot library, they have something like this. If you think it is not capable for achieving this feature, you can also introduce a simple database like SQLite to achieve this.

### Break time

After one tomato clock ends, we usually have some break time. I would like you to add a break time management system.

For each user:

1. They have their own break time.

2. They can modify it in the settings.

3. The default time is 5 minutes.