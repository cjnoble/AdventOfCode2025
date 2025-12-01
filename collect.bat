@echo off
REM script for daily collect content of problem of AOC
REM inputs are: DAY, YEAR (need to respect the order)

REM Check if there are exactly two arguments
if "%1"=="" (
  echo Need two input arguments in the following order: collect ^<day^> ^<year^>
  exit /b 1
)

REM Set the DAY and YEAR variables
set DAY=%1
set YEAR=%2

REM Run the Python script
python daily_collect.py -d %DAY% -y %YEAR%
