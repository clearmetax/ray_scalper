@echo off
color 0A

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Check if .env file exists
if not exist .env (
    echo Creating .env file...
    echo PRIVATE_KEY=your_private_key_here > .env
    echo RPC_URL=your_rpc_url_here >> .env
    echo SPIDER_SWAP_URL=https://api.spiderswap.com/v1/swap >> .env
    echo SPIDER_SWAP_API_KEY=your_api_key_here >> .env
    echo SOL_ADDRESS=So11111111111111111111111111111111111111112 >> .env
    echo Please edit the .env file with your credentials before starting the bot.
    pause
    exit /b 1
)

REM Start the bot
python menu.py

REM Deactivate virtual environment
deactivate

pause 