import webbrowser
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta
import time


def birthday_message(name):
    return f"""🎉 Praise the Lord {name},

Wishing you a very Happy Birthday!

"May the Lord bless you and keep you."
— Numbers 6:24

May Jesus Christ fill your life with His peace, joy and abundant blessings.

Blessings & Prayers,

Christ Methodist Church
Rev. S. K. Masih
"""


def anniversary_message(name):
    return f"""💍 Praise the Lord {name},

Happy Wedding Anniversary!

"Therefore what God has joined together, let no one separate."
— Mark 10:9

May the Lord strengthen your marriage with love, peace and His everlasting grace.

Blessings & Prayers,

Christ Methodist Church
Rev. S. K. Masih
"""


def send_whatsapp(phone, message):

    phone = str(phone).strip()

    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    phone = phone.replace("+", "")

    url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

    webbrowser.open(url)


def send_all_whatsapp(excel_file):

    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()

    today = datetime.today()

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    count = 0

    for _, row in df.iterrows():

        phone = row["MOBILE NUMBER"]

        # Birthday
        if pd.notna(row["BIRTHDAY DATE"]):

            d = pd.to_datetime(row["BIRTHDAY DATE"])

            try:
                next_date = d.replace(year=today.year)
            except:
                continue

            if week_start <= next_date <= week_end:
                send_whatsapp(phone, birthday_message(row["NAME"]))
                count += 1
                time.sleep(2)

        # Anniversary
        if pd.notna(row["ANNIVERSARY DATE"]):

            d = pd.to_datetime(row["ANNIVERSARY DATE"])

            try:
                next_date = d.replace(year=today.year)
            except:
                continue

            if week_start <= next_date <= week_end:
                send_whatsapp(phone, anniversary_message(row["NAME"]))
                count += 1
                time.sleep(2)

    print(f"{count} WhatsApp chats opened.")
    
    if __name__ == "__main__":
               send_whatsapp("919319966155", "Test Message")