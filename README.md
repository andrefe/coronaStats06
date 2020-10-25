# Setup

## debian/ubuntu

Python 3 is required to run corona_stat: just run the following commands
```
$ ./INSTALL.sh
```

If you want to start corona_stats as web application, run
```
$ source venv/bin/activate
$ flask run

# to quit venv
$ deactivate
```

If you want to start corona_stats as standalone script, run
```
$ source venv/bin/activate
$ ./main.py

# to quit venv
$ deactivate
```

## WSL

Install your favourite WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10

Download XServer for windows: https://sourceforge.net/projects/xming/

Do not forget to redirect your output to the (just installed) X server 
```
export DISPLAY=localhost:0.0
```
