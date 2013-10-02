# Scpd-scraper-v2

This is a simple script to download scpd videos. The basic usage is:


```
python scraper.py course_name1 course_name2 ...
```

The program will prompt for your SuID and password. If two-step authentication is enabled for your account, it will also prompt for the authentication code. Watch the terminal for the prompt after you have authenticated yourself with your id and password.

There is one dependency for this script:

* selenium

You can use the ```requirements.txt``` file in the repo to install it:

```
pip install -r requirements.txt
```

The script is inspired by [scpd-scraper](https://github.com/jkeesh/scpd-scraper).
