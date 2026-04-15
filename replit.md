# Textile Bale Bot

A Python-based Telegram bot for generating and tracking bale numbers for various fabric types.

## Overview

The bot provides an interactive Telegram interface using inline keyboards to select fabric types and generate sequential bale numbers (e.g., `10-001` for Knitted Plain).

## Fabric Types & Codes

| Fabric | Code |
|--------|------|
| Knitted Plain | 10 |
| Knitted Print | 11 |
| Satin Plain | 20 |
| Satin Print | 21 |
| Linen Plain | 30 |
| Linen Print | 31 |
| Twill Plain | 40 |
| Twill Print | 41 |
| Dobby Plain | 50 |
| Dobby Print | 51 |
| Fent | 60 |
| 1M | 70 |

## Tech Stack

- **Language**: Python 3.12
- **Framework**: python-telegram-bot 20.3
- **Dependencies**: gspread, google-auth (for optional Google Sheets integration)

## Environment Variables

- `TELEGRAM_TOKEN` (required): Telegram Bot API token from @BotFather
- `ADMIN_USER_ID` (optional): Telegram user ID of the admin (defaults to 123456789)

## Running

The bot runs as a console workflow via `python bale_bot.py`. It uses long-polling to receive Telegram updates.

## Commands

- `/start` - Shows the fabric selection menu
- `/help` - Shows available commands

## Notes

- Bale counters are stored in memory and reset on restart
- The Google Sheets credentials file (`textile-bale-bot-*.json`) is present for potential persistence integration
