# ~~OP.GG~~ League of Legends Build Finder

To install prerequisites, do `pip install -r requirements.txt`.

This is a tool to find builds for specific champions from the best one-tricks. It uses OP.GG or U.GG (your choice!) to find a list of the top 5 players and chooses from them in the following priority:

1. Highest rank and LP
2. Highest winrate
3. Most games played

Then, the program will open the player's profile in the user's default web browser.

Please note that this tool was developed for **ARAM**. Champion builds are dependent on matchups, elos, and regions, so use for ranked at your own risk.

## Notes

* **Requests & Beautiful Soup**: The information I want to scrape is part of JavaScript data that is loaded dynamically. Thus, the Requests library won't work, since it only gets static HTML elements.

* **Selenium**: Does everything I wanted to do, but found it to be significantly slower at loading a webpage than Playwright.

* **NamedTuple**: A "Player" was originally a class, but it didn't really need to be since its only method was to print out its information. A NamedTuple is just slightly less overhead.

* **OP.GG or U.GG?**: U.GG is a slightly more responsive website, so the U.GG build finder will be faster most of the time.

## Difficulties

* **Speed**: The program now takes ~4-5 seconds, which is pretty quick, but I do wish it was 2 seconds or faster.

* **Async**: Still having trouble with implementing async, but the program is small enough that I (think?) the program wouldn't be much faster with it. This is also quite complicated to implement with tkinter.

* **Distribution**: I wanted to make the program a `.exe` file for one other person to use, but every program I tried (Nuitka, Cython, PyInstaller, etc.) was always flagged as a virus by Windows Defender, even if I didn't use `-onefile`. This is because the way these programs pack the files together is similar to the way malware is packed.

    Possible solutions:
    1. Encryption
    2. Create an exception in antivirus
    3. Message Microsoft with the program and they can create a global exception
    4. Signature!

## Credits

* **CenterWindowToDisplay()**: This function was taken from another [post](https://github.com/TomSchimansky/CustomTkinter/discussions/1820).
