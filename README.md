# OP.GG Build Finder

To install prerequisites, do `pip install -r requirements.txt`.

This is a tool to find builds for specific champions from the best one-tricks. It uses OP.GG to find a list of players and chooses from them in the following priority:

1. Highest rank
2. Highest winrate
3. Most games played

Then, the program will open the player's OP.GG profile in the user's default web browser.

Please note that it only scrapes information from the top 3 players on OP.GG. The way to retrive information from players below the top 3 changes frequently enough that I decided to not keep updating the program for it.

## Notes

* Requests & Beautiful Soup
The information I want to scrape is part of JavaScript data that is loaded dynamically. Thus, the Requests library won't work, since it only gets static HTML elements.

* Selenium
Does everything I wanted to do, but found it to be significantly slower at loading a webpage than Playwright.

* NamedTuple
A "Player" was originally a class, but it didn't really need to be since its only method was to print out its information. A NamedTuple is just slightly less overhead.

## Difficulties

* Speed
The program takes ~10 seconds the first time it is ran. Afterwards, it takes ~4-6 seconds, which is not fast enough.

* Async
Still having trouble with implementing async, but the program is small enough that I (think?) the program wouldn't be much faster with it.

* Distribution
I wanted to make the program a `.exe` file for someone else to use, but every program I tried (Nuitka, Cython, PyInstaller, etc.) was always flagged as a virus by Windows Defender, even if I didn't use `-onefile`. This is because the way these programs pack the files together is similar to the way malware is packed.

Possible solutions:
1. Encryption
2. Create an exception in antivirus
3. Message Microsoft with the program and they can create a global exception

## Credits

* CenterWindowToDisplay()
This function was taken from another [post](https://github.com/TomSchimansky/CustomTkinter/discussions/1820) on GitHub.
