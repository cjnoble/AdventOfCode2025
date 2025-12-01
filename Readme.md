# Advent Of Code 2025

Repo for advent of code 2025

## Automation

### Caching

All inputs are cached locally  

### User agent info

User agent info is set from environment variables

create a .env file and set:
`AOC_USER_AGENT=<https://github.com/username/AdventOfCode2025 by email@example.com>

### Throttling

Download is only triggered once each time the script is run - so don't keep rerunning it

### Session cookie

During your first query, the script will ask for your session token in order to download the input file. To get you session token, you need to follow the following steps :

- go to the AOC website and inspect page (F12)
- go to the "network" section in the inspector (top right)
- login and click to "login" request in the inspector (left side)
- check for subsection "cookies" in the "network" section in inspector (right side)
- get the "session" value and paste it in the terminal
- Your session token will automatically be saved in the hidden cache file .session_cache.lock

## Retrieval of the daily problem

    #./collect day year
    ./collect 1 2025
