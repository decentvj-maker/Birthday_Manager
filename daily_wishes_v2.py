import webbrowser
import urllib.parse
import pandas as pd

from datetime import datetime

from tkinter import (
    Toplevel,
    Text,
    END,
    messagebox,
    ttk
)

# -----------------------------
# TEST MODE
# -----------------------------
TEST_MODE = True


def birthday_message(name):

    return f"""Dear {name},

Wishing you a Blessed Birthday!

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
        messagebox.showerror("Error", str(e))
        return

    df.columns = df.columns.str.strip()

    df["BIRTHDAY DATE"] = pd.to_datetime(
        df["BIRTHDAY DATE"],
        errors="coerce"
    )

    df["ANNIVERSARY DATE"] = pd.to_datetime(
        df["ANNIVERSARY DATE"],
        errors="coerce"
    )

    today = datetime.today()

    birthdays = []
    anniversaries = []

    if TEST_MODE:

        for _, row in df.iterrows():

            # Birthday sirf tab add karo jab date ho
            if pd.notna(row["BIRTHDAY DATE"]):
                birthdays.append(
                    (
                        row["NAME"],
                        str(row["MOBILE NUMBER"])
                    )
                )

            # Anniversary sirf tab add karo jab date ho
            if pd.notna(row["ANNIVERSARY DATE"]):
                anniversaries.append(
                    (
                        row["NAME"],
                        str(row["MOBILE NUMBER"])
                    )
                )

    else:
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

    win = Toplevel()

    win.title("Daily Wishes Center")

    win.geometry("760x650")

    ttk.Label(
        win,
        text="Today's Birthdays",
        font=("Arial",14,"bold")
    ).pack(pady=8)

    tree1 = ttk.Treeview(
        win,
        columns=("Name","Mobile"),
        show="headings",
        height=8
    )

    tree1.heading("Name", text="Name")
    tree1.heading("Mobile", text="Mobile")

    tree1.column("Name", width=330)
    tree1.column("Mobile", width=180)

    tree1.pack(fill="x", padx=15)

    for item in birthdays:
        tree1.insert("", END, values=item)

    ttk.Label(
        win,
        text="Today's Anniversaries",
        font=("Arial",14,"bold")
    ).pack(pady=10)

    tree2 = ttk.Treeview(
        win,
        columns=("Name","Mobile"),
        show="headings",
        height=8
    )

    tree2.heading("Name", text="Name")
    tree2.heading("Mobile", text="Mobile")

    tree2.column("Name", width=330)
    tree2.column("Mobile", width=180)

    tree2.pack(fill="x", padx=15)

    for item in anniversaries:
        tree2.insert("", END, values=item)
    if TEST_MODE:

        for _, row in df.iterrows():

            birthdays.append(
                (
                    row["NAME"],
                    str(row["MOBILE NUMBER"])
                )
            )

            anniversaries.append(
                (
                    row["NAME"],
                    str(row["MOBILE NUMBER"])
                )
            )

    else:

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

    win = Toplevel()

    win.title("Daily Wishes Center")

    win.geometry("760x650")

    ttk.Label(
        win,
        text="Today's Birthdays",
        font=("Arial", 14, "bold")
    ).pack(pady=8)

    tree1 = ttk.Treeview(
        win,
        columns=("Name", "Mobile"),
        show="headings",
        height=8
    )

    tree1.heading("Name", text="Name")
    tree1.heading("Mobile", text="Mobile")

    tree1.column("Name", width=330)
    tree1.column("Mobile", width=180)

    tree1.pack(fill="x", padx=15)

    for item in birthdays:
        tree1.insert("", END, values=item)

    ttk.Label(
        win,
        text="Today's Anniversaries",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tree2 = ttk.Treeview(
        win,
        columns=("Name", "Mobile"),
        show="headings",
        height=8
    )

    tree2.heading("Name", text="Name")
    tree2.heading("Mobile", text="Mobile")

    tree2.column("Name", width=330)
    tree2.column("Mobile", width=180)

    tree2.pack(fill="x", padx=15)

    for item in anniversaries:
        tree2.insert("", END, values=item)

        def preview_message():

            birthday_selected = tree1.focus()
            anniversary_selected = tree2.focus()

        # Dono select hain
        if birthday_selected != "" and anniversary_selected != "":
            messagebox.showwarning(
                "Warning",
                "Please select only one member."
            )
            return

        # Birthday Preview
        if birthday_selected != "":

            values = tree1.item(birthday_selected)["values"]

            msg = birthday_message(values[0])

            top = Toplevel(win)
            top.title("Birthday Preview")
            top.geometry("600x500")

            txt = Text(
                top,
                wrap="word",
                font=("Arial",11)
            )

            txt.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            txt.insert("1.0", msg)
            txt.config(state="disabled")

            return

        # Anniversary Preview
        if anniversary_selected != "":

            values = tree2.item(anniversary_selected)["values"]

            msg = anniversary_message(values[0])

            top = Toplevel(win)
            top.title("Anniversary Preview")
            top.geometry("600x500")

            txt = Text(
                top,
                wrap="word",
                font=("Arial",11)
            )

            txt.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            txt.insert("1.0", msg)
            txt.config(state="disabled")

            return

        messagebox.showwarning(
            "Warning",
            "Please select a member."
        )
    def send_all():

        if messagebox.askyesno(
            "Confirmation",
            "Send wishes to all members shown?"
        ) == False:
            return

        for child in tree1.get_children():

            values = tree1.item(child)["values"]

            mobile = str(values[1]).replace(".0", "")

            msg = birthday_message(values[0])

            url = (
                "https://wa.me/"
                + mobile
                + "?text="
                + urllib.parse.quote(msg)
            )

            webbrowser.open(url)

        for child in tree2.get_children():

            values = tree2.item(child)["values"]

            mobile = str(values[1]).replace(".0", "")

            msg = anniversary_message(values[0])

            url = (
                "https://wa.me/"
                + mobile
                + "?text="
                + urllib.parse.quote(msg)
            )

            webbrowser.open(url)

    frame = ttk.Frame(win)
    frame.pack(pady=15)

    ttk.Button(
        frame,
        text="Preview",
        command=preview_message
    ).pack(side="left", padx=5)

    ttk.Button(
        frame,
        text="Send Selected",
        command=send_selected
    ).pack(side="left", padx=5)

    ttk.Button(
        frame,
        text="Send All",
        command=send_all
    ).pack(side="left", padx=5)

    ttk.Button(
        frame,
        text="Close",
        command=win.destroy
    ).pack(side="left", padx=5)

    ttk.Label(
        win,
        text=f"Birthdays : {len(birthdays)}    |    Anniversaries : {len(anniversaries)}",
        font=("Arial",10,"bold")
    ).pack(pady=10)

    if len(birthdays) == 0 and len(anniversaries) == 0:

        messagebox.showinfo(
            "Daily Wishes",
            "No Birthdays or Anniversaries Found."
        )        
