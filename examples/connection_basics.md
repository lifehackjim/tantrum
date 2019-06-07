# Connection basics

First, create a file named tantrum_creds.py that has the following:
```
url = "https://192.168.1.32"
username = "USERNAME"
password = "PASSWORD"
```

Then run tantrum_shell.py in python interactive mode to get an adapter established:
```
pipenv run python3 -i tantrum_shell.py
```

This will provide an ``adapter`` object, which is used by workflows or can be used directly as is.
