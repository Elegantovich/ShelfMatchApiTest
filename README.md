# ShelfMatchApiTest

![Status](https://github.com/elegantovich/ShelfMatchApiTest/actions/workflows/main.yml/badge.svg)
## Description
Скрипт для распознавания товаров с полок магазинов, работающий по API.

### Tech
Python 3.10, requests 2.28, ShelfMatchApi


### How to start a project:

Clone and move to local repository:

```
git clone https://github.com/Elegantovich/ShelfMatchApiTest/
```
Create a virtual environment (win):
```
python -m venv venv
```
Activate a virtual environment:
```
source venv/Scripts/activate
```
Create a file use the `.env` command and add environment variables to it to work with the script (test credentials from the TOR have already been entered by default):
```
touch .env
```
Install dependencies from file requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Run the script
```
python test.py
```
