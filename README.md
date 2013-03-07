# Life-Logger Manifesto
~~This is a work in progress and is definitely not usable.~~ _If you want to look around and help out or tell me how I could improve the code, feel free._

__Life-Logger is a terminal utility to track your day in one-liners, à la Twitter or version control commits.__



## Its differentiating features are:
* __It is a life logger, not a time tracker.__ You are encouraged and supposed to enter all significant actions performed during a day.
* __Logging is extremely fast and simple.__ The only required parameter is the title. Starting time and ending time are automatically calculated based on the ending time of the previous activity and the actual time of the log.
* __You maintain control over your data and it is always accessible and exportable.__ Everything is logged in a single _.txt_ file, so that you can edit it with any text editor that you want or export it somewhere else. You decide who you share it with.

## Features in:
* Log an action
* Tag your logs
* Filter logs by tag, date or any partial query
* View the number of hours spent

![Screenshot](http://img705.imageshack.us/img705/9228/lifeloggerscreenshot.png "Example Screenshot")

## Ideas for possible future features:
* Filter and view all logs within a set time interval
* Show a graphic of the amount of hours spent on a chosen tag (all-time or within an optional time interval)
* Export/Publish as html+css
* Different kinds of entries: action log, summary of the day, idea, ...


## Installation instructions:
_Requirements:_ Python (no version testing yet).

All you need to do is clone the repository or download ``life_logger.py`` to a folder in which you have writing permission. If you don't know what this is about, just do the following:

1. Fire up your terminal
2. Paste + intro: ``git clone https://github.com/mvime/life_logger.git && cd life_logger``

Installed! Now:

1. Log your first action by pasting + intro: ``python life_logger.py "Tried out Life-Logger"``
2. Check out the section on Syntax & Examples to learn about all the options!

## Syntax & Examples:
* Log an action: ``python life_logger.py "Tried out Life-Logger"``
* Log an action, setting the start-time: ``python life_logger.py "Went out running" start:-1.25h``
* Log an action, with tags: ``python life_logger.py "Translated the MISA manuscript" @work @translation @MISAproject @client-name``
* View all logs: ``python life_logger.py --view-all``
* View last X logs: ``python life_logger.py --last-X`` (replace X with any number)
* View all logs tagged @work: ``python life_logger.py --view-all @work``
* Catch-up, to be used when you haven't been able to log in a while: ``python life_logger.py --catch-up`` (See the huge screenshot below to better understand what it does)

![Screenshot](http://img202.imageshack.us/img202/4922/catchupexample.png "--catch-up option example")
