# Scpd-scraper-v2

This is a simple script to download scpd videos. The basic usage is:


```
python scraper.py course_name1 course_name2 ...
```

There are several requirements for the script:

* [selenium](https://pypi.python.org/pypi/selenium). You can use ``` pip install -r requirements.txt ``` to install it using the ``` requirements.txt``` in the repo.
* [Firefox](https://www.mozilla.org/en-US/firefox/new/)
* [mimms](http://savannah.nongnu.org/projects/mimms/)

The program will prompt for your SuID and password. If two-step authentication is enabled for your account, it will also prompt for the authentication code. Watch the terminal for the prompt after you have authenticated yourself with your id and password.

The script is inspired by [scpd-scraper](https://github.com/jkeesh/scpd-scraper).
