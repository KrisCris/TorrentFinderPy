# Torrent Finder

## What is it

A simple Python script that walks through a directory and its subdirectories, opens each `.torrent` file, decodes it, and checks the `name` field in the torrent file's `info` dictionary. Matched files will be printed out.

## How to Use

- Install `Python 3.11.4` (Lower version may also work, IDK)
- Go into the folder and init environment: `python3 -m venv venv`
- Activate the environment
  - Linux/macOS:
    - `cd` into the project folder
    - `source ./venv/bin/activate`
  - Windows:
    - Open `cmd`,
    - Navigate to the folder
    - Run `.\venv\Scripts\activate` (maybe)
- Install requirements `pip install -r "requirements.txt"`
- Run the script:

    ```python
    python main.py -p "/path/to/search" -n "^regex pattern to find$"
    ```
