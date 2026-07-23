import webbrowser
import urllib.parse
import pandas as pd
from datetime import datetime
from tkinter import (
    Toplevel,
    ttk,
    messagebox,
    Text,
    END
)


def birthday_message(name):

    return f"""Dear {name},

Wishing you a blessed Birthday!

"This is the day the Lord has made;
let us rejoice and be glad in it."
(Psalm 118:24)

May God bless you with good health,
peace, wisdom and abundant grace.

Blessings & Prayers,

Christ Methodist Church
Rev. S. K. Masih
"""


def anniversary_message(name):

    return f"""Dear {name},

Happy Wedding Anniversary!

"Therefore what God has joined together,
let no one separate."
(Mark 10:9)

May the Lord continue to bless your
marriage with love, unity and His grace.

Blessings & Prayers,

Christ Methodist Church
Rev. S. K. Masih
"""


def open_daily_wishes(excel_file):

    if excel_file == "":
        messagebox.showwarning(
            "Warning",
            "Please Select Excel File"
        )
        return

    try:

        df = pd.read_excel(excel_file)

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        return

    df.columns = df.columns.str.strip()

    required = [
        "NAME",
        "MOBILE NUMBER",
        "BIRTHDAY DATE",
        "ANNIVERSARY DATE"
    ]

    for col in required:

        if col not in df.columns:

            messagebox.showerror(
                "Error",
                f"{col} not found."
            )

            return

    df["BIRTHDAY DATE"] = pd.to_datetime(
        df["BIRTHDAY DATE"],
        errors="coerce"
    )

    df["ANNIVERSARY DATE"] = pd.to_datetime(
        df["ANNIVERSARY DATE"],
        errors="coerce"
    )

    today = datetime.today()
    # ---------------- TEST MODE ----------------

TEST_MODE = True

if TEST_MODE:

    birthdays = []

    anniversaries = []

    for _, row in df.iterrows():

        birthdays.append(
            (
                row["NAME"],
                str(row["MOBILE NUMBER"])
            )
        )

        if pd.notna(row["ANNIVERSARY DATE"]):

            anniversaries.append(
                (
                    row["NAME"],
                    str(row["MOBILE NUMBER"])
                )
            )

else:

    birthdays = []

    anniversaries = []

    for _, row in df.iterrows():

        if pd.notna(row["BIRTHDAY DATE"]):

            d = row["BIRTHDAY DATE"]

            if d.day == today.day and d.month == today.month:

                birthdays.append(
                    (
                        row["NAME"],
                        str(row["MOBILE NUMBER"])
                    )
                )

        if pd.notna(row["ANNIVERSARY DATE"]):

            d = row["ANNIVERSARY DATE"]

            if d.day == today.day and d.month == today.month:

                anniversaries.append(
                    (
                        row["NAME"],
                        str(row["MOBILE NUMBER"])
                    )
                )

    
        if pd.notna(row["BIRTHDAY DATE"]):

            d = row["BIRTHDAY DATE"]

            if d.day == today.day and d.month == today.month:

                birthdays.append(

                    (
                        row["NAME"],
                        str(row["MOBILE NUMBER"])
                    )

                )

        if pd.notna(row["ANNIVERSARY DATE"]):

            d = row["ANNIVERSARY DATE"]

            if d.day == today.day and d.month == today.month:

                anniversaries.append(

                    (
                        row["NAME"],
                        str(row["MOBILE NUMBER"])
                    )

                )

    win = Toplevel()

    win.title("Daily Wishes Center")

    win.geometry("760x620")

    ttk.Label(

        win,

        text="Today's Birthdays",

        font=("Arial",14,"bold")

    ).pack(
        pady=8
    )

    tree1 = ttk.Treeview(

        win,

        columns=("Name","Mobile"),

        show="headings",

        height=7

    )

    tree1.heading(

        "Name",

        text="Name"

    )

    tree1.heading(

        "Mobile",

        text="Mobile"

    )

    tree1.column(

        "Name",

        width=320

    )

    tree1.column(

        "Mobile",

        width=180

    )

    tree1.pack(
        fill="x",
        padx=15
    )

    for item in birthdays:

        tree1.insert(

            "",

            END,

            values=item

        )
            # ---------------- Today's Anniversaries ----------------

    ttk.Label(
        win,
        text="Today's Anniversaries",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tree2 = ttk.Treeview(
        win,
        columns=("Name", "Mobile"),
        show="headings",
        height=7
    )

    tree2.heading("Name", text="Name")
    tree2.heading("Mobile", text="Mobile")

    tree2.column("Name", width=320)
    tree2.column("Mobile", width=180)

    tree2.pack(
        fill="x",
        padx=15
    )

    for item in anniversaries:

        tree2.insert(
            "",
            END,
            values=item
        )

    # ---------------- Preview ----------------
    def send_selected():

     selected = tree1.focus()

    wish_type = "Birthday"

    if selected == "":
        selected = tree2.focus()
        wish_type = "Anniversary"

    if selected == "":
        messagebox.showwarning(
            "Warning",
            "Please select a member."
        )
        return

    if wish_type == "Birthday":
        values = tree1.item(selected)["values"]
    else:
        values = tree2.item(selected)["values"]

    name = values[0]
    mobile = str(values[1])

    mobile = mobile.replace(".0", "")

    if wish_type == "Birthday":
        msg = birthday_message(name)
    else:
        msg = anniversary_message(name)

    answer = messagebox.askyesno(

        "Confirmation",

        f"Send WhatsApp to\n\n{name} ?"

    )

    if not answer:
        return

    url = "https://wa.me/" + mobile + "?text=" + urllib.parse.quote(msg)

    webbrowser.open(url)

    def preview_message():

        wish_type = None
        values = None

        selected = tree1.focus()

        if selected:

            values = tree1.item(selected)["values"]
            wish_type = "Birthday"

        else:

            selected = tree2.focus()

            if selected:

                values = tree2.item(selected)["values"]
                wish_type = "Anniversary"

        if values is None:

            messagebox.showwarning(
                "Warning",
                "Please select a member."
            )
            return

        name = values[0]

        if wish_type == "Birthday":

            msg = birthday_message(name)

        else:

            msg = anniversary_message(name)

        top = Toplevel(win)

        top.title("Preview Message")

        top.geometry("600x500")

        txt = Text(
            top,
            wrap="word",
            font=("Arial", 11)
        )

        txt.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        txt.insert(
            "1.0",
            msg
        )

        txt.config(state="disabled")
            # ---------------- Buttons ----------------

    button_frame = ttk.Frame(win)

    button_frame.pack(
        pady=15
    )

    ttk.Button(
        button_frame,
        text="Preview",
        command=preview_message
    ).pack(
        side="left",
        padx=10
    )

    ttk.Button(
        button_frame,
        text="Send Selected",
        command=send_selected(
            "Coming Soon",
            "WhatsApp Module will be added in Version 2."
        )
    ).pack(
        side="left",
        padx=10
    )

    ttk.Button(
        button_frame,
        text="Close",
        command=win.destroy
    ).pack(
        side="left",
        padx=10
    )

    # ---------------- Summary ----------------

    ttk.Label(
        win,
        text=f"Today's Birthdays : {len(birthdays)}",
        font=("Arial",10,"bold")
    ).pack()

    ttk.Label(
        win,
        text=f"Today's Anniversaries : {len(anniversaries)}",
        font=("Arial",10,"bold")
    ).pack()

    # ---------------- Empty List ----------------

    if len(birthdays) == 0 and len(anniversaries) == 0:

        messagebox.showinfo(
            "Daily Wishes",
            "No Birthdays or Anniversaries Today."
        )

    win.focus()