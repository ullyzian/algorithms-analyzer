# Algorithm Analyzer

# UWAGA: Nie udało mi się skompilować program sprawdzianu, bo mam MacOs

# Setup

Create virtual environment and install dependencies
```shell script
$ poetry install
```

Run application
```shell script
$ python main.py
```


## Bundle app

Create apps for Mac (app and shell exec), Windows and Linux

```shell script
$ pyinstaller main.spec
```
After that you can find executable files for your system in `dist/` folder