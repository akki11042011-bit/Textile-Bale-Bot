#!/usr/bin/env python3
"""
<<<<<<< HEAD
TEXTILE BALE BOT
- Fixed typing compatibility for Python 3.12+
- Persistent counters via JSON file (survives Render restarts)
=======
TEXTILE BALE BOT - With Google Sheets persistence
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)
"""

import logging
import os
import json

<<<<<<< HEAD
=======
import gspread
from google.oauth2.service_account import Credentials
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

<<<<<<< HEAD
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8586325828:AAEykeKro3p_WpxsYULeS96hbzTRGrmrRak")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "557786947"))
COUNTER_FILE = os.getenv("COUNTER_FILE", "bale_counters.json")
=======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)

BALE_CODES = {
    "Knitted Plain": "10",
    "Knitted Print": "11",
    "Satin Plain": "20",
    "Satin Print": "21",
    "Linen Plain": "30",
    "Linen Print": "31",
    "Twill Plain": "40",
    "Twill Print": "41",
    "Dobby Plain": "50",
    "Dobby Print": "51",
    "Fent": "60",
    "1M": "70",
}

<<<<<<< HEAD
# --- Persistent counters ---

def load_counters():
    try:
        with open(COUNTER_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_counters(counters):
    with open(COUNTER_FILE, "w") as f:
        json.dump(counters, f)

counters = load_counters()
=======
counters = {}
sheet = None

SERVICE_ACCOUNT_FILE = "textile-bale-bot-479473ba5e14.json"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def init_sheets():
    global sheet, counters
    if not GOOGLE_SHEETS_ID:
        logger.warning("GOOGLE_SHEETS_ID not set - using in-memory counters only")
        return
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(GOOGLE_SHEETS_ID)

        try:
            sheet = spreadsheet.worksheet("Counters")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="Counters", rows=50, cols=2)
            sheet.update("A1:B1", [["Code", "Count"]])
            logger.info("Created 'Counters' worksheet")

        records = sheet.get_all_values()
        for row in records[1:]:
            if len(row) >= 2 and row[0] and row[1]:
                try:
                    counters[row[0]] = int(row[1])
                except ValueError:
                    pass

        for code in BALE_CODES.values():
            if code not in counters:
                counters[code] = 0

        logger.info(f"Loaded counters from Google Sheets: {counters}")
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets: {e}")
        sheet = None


def save_counter(code, value):
    if sheet is None:
        return
    try:
        records = sheet.get_all_values()
        for i, row in enumerate(records[1:], start=2):
            if row and row[0] == code:
                sheet.update_cell(i, 2, value)
                return
        sheet.append_row([code, value])
    except Exception as e:
        logger.error(f"Failed to save counter to Google Sheets: {e}")

>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)

def get_bale_number(code):
    if code not in counters:
        counters[code] = 0
    counters[code] += 1
<<<<<<< HEAD
    save_counters(counters)
    return f"{code}-{str(counters[code]).zfill(3)}"

# --- Handlers ---

async def start(update, context):
=======
    save_counter(code, counters[code])
    return f"{code}-{str(counters[code]).zfill(3)}"


def build_main_menu():
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)
    buttons = []
    items = list(BALE_CODES.keys())
    for i in range(0, len(items), 3):
        row = []
        for j in range(3):
            if i + j < len(items):
                item = items[i + j]
                row.append(InlineKeyboardButton(item, callback_data=item))
        if row:
            buttons.append(row)
<<<<<<< HEAD

    buttons.append([InlineKeyboardButton("📊 Status", callback_data="status")])

=======
    buttons.append([InlineKeyboardButton("📊 Status", callback_data="status")])
    return InlineKeyboardMarkup(buttons)


async def start(update, context):
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)
    msg = "🧵 TEXTILE BALE GENERATOR\n\nSelect fabric type:"
    await update.message.reply_text(msg, reply_markup=build_main_menu())


async def button_press(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "status":
        msg = "📊 STATUS\n\n"
        for name, code in BALE_CODES.items():
            last = counters.get(code, 0)
<<<<<<< HEAD
            msg += f"{code}: {code}-{str(last).zfill(3)}\n"

        await query.edit_message_text(
            msg,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Menu", callback_data="menu")]]
            ),
        )

    elif query.data == "menu":
        buttons = []
        items = list(BALE_CODES.keys())
        for i in range(0, len(items), 3):
            row = []
            for j in range(3):
                if i + j < len(items):
                    item = items[i + j]
                    row.append(InlineKeyboardButton(item, callback_data=item))
            if row:
                buttons.append(row)
        buttons.append([InlineKeyboardButton("📊 Status", callback_data="status")])

        msg = "🧵 TEXTILE BALE GENERATOR\n\nSelect fabric type:"
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
=======
            msg += f"{name} ({code}): {code}-{str(last).zfill(3)}\n"
        back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menu", callback_data="menu")]])
        await query.edit_message_text(msg, reply_markup=back_btn)

    elif query.data == "menu":
        msg = "🧵 TEXTILE BALE GENERATOR\n\nSelect fabric type:"
        await query.edit_message_text(msg, reply_markup=build_main_menu())
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)

    elif query.data in BALE_CODES:
        code = BALE_CODES[query.data]
        bale_no = get_bale_number(code)
<<<<<<< HEAD

=======
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)
        msg = f"✅ Bale Generated\n{query.data}\nNo: {bale_no}"
        buttons = [
            [InlineKeyboardButton(f"🔄 Again {query.data}", callback_data=query.data)],
            [InlineKeyboardButton("⬅️ Menu", callback_data="menu")],
        ]
<<<<<<< HEAD

=======
>>>>>>> 81c7774 (Integrate Google Sheets for persistent storage of bale counters)
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))


async def help_cmd(update, context):
    msg = "Commands:\n/start - Menu\n/help - This"
    await update.message.reply_text(msg)


def main():
    logger.info("Starting...")
    init_sheets()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(button_press))
    logger.info("Bot started successfully")
    app.run_polling()


if __name__ == "__main__":
    main()
