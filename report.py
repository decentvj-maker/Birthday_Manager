import pandas as pd
from print_report import print_pdf
from pdf_report import export_pdf
from tkinter import Toplevel, ttk, messagebox
from datetime import datetime, timedelta


def generate_weekly_report(excel_file):

    # Read Excel
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    # Remove empty spaces from column names
    df.columns = df.columns.str.strip()

    # Column names
    name_col = "NAME"
    birthday_col = "BIRTHDAY DATE"
    anniversary_col = "ANNIVERSARY DATE"
    mobile_col = "MOBILE NUMBER"

    # Check required columns
    required = [name_col, birthday_col, anniversary_col]

    for col in required:
        if col not in df.columns:
            messagebox.showerror(
                "Error",
                f"Column '{col}' not found.\n\nAvailable Columns:\n\n{list(df.columns)}"
            )
            return

    # Convert dates
    df[birthday_col] = pd.to_datetime(df[birthday_col], errors="coerce")
    df[anniversary_col] = pd.to_datetime(df[anniversary_col], errors="coerce")

    today = datetime.today()

    # Current week Monday
    week_start = today - timedelta(days=today.weekday())

    # Current week Sunday
    week_end = week_start + timedelta(days=6)

    birthdays = []
    anniversaries = []

    for _, row in df.iterrows():

        # Birthday
        if pd.notna(row[birthday_col]):

            d = row[birthday_col]

            try:
                next_date = d.replace(year=today.year)
            except:
                continue

            if next_date < today:
                next_date = next_date.replace(year=today.year + 1)

            if week_start.date() <= next_date.date() <= week_end.date():
                birthdays.append((
                    row[name_col],
                    next_date.strftime("%d-%b"),
                    str(row.get(mobile_col, ""))
                ))

        # Anniversary
        if pd.notna(row[anniversary_col]):

            d = row[anniversary_col]

            try:
                next_date = d.replace(year=today.year)
            except:
                continue

            if next_date < today:
                next_date = next_date.replace(year=today.year + 1)

            if week_start.date() <= next_date.date() <= week_end.date():
                anniversaries.append((
                    row[name_col],
                    next_date.strftime("%d-%b"),
                    str(row.get(mobile_col, ""))
                ))

    # Report Window

    win = Toplevel()
    win.title("Weekly Report")
    win.geometry("700x550")

    ttk.Label(
    win,
    text=f"Birthdays ({week_start.strftime('%d-%b')} to {week_end.strftime('%d-%b')})",
    font=("Arial", 14, "bold")
    ).pack(pady=5)

    tree1 = ttk.Treeview(
        win,
        columns=("Name", "Date", "Mobile"),
        show="headings",
        height=8
    )

    tree1.heading("Name", text="Name")
    tree1.heading("Date", text="Date")
    tree1.heading("Mobile", text="Mobile")

    tree1.column("Name", width=250)
    tree1.column("Date", width=100)
    tree1.column("Mobile", width=150)

    tree1.pack(fill="x", padx=10)

    for item in birthdays:
        tree1.insert("", "end", values=item)

    ttk.Label(
    win,
    text=f"Anniversaries ({week_start.strftime('%d-%b')} to {week_end.strftime('%d-%b')})",
    font=("Arial", 14, "bold")
    ).pack(pady=10)

    tree2 = ttk.Treeview(
        win,
        columns=("Name", "Date", "Mobile"),
        show="headings",
        height=8
    )

    tree2.heading("Name", text="Name")
    tree2.heading("Date", text="Date")
    tree2.heading("Mobile", text="Mobile")

    tree2.column("Name", width=250)
    tree2.column("Date", width=100)
    tree2.column("Mobile", width=150)

    tree2.pack(fill="x", padx=10)

    for item in anniversaries:
        tree2.insert("", "end", values=item)

    if len(birthdays) == 0 and len(anniversaries) == 0:
        messagebox.showinfo(
            "Information",
            "No Birthday or Anniversary in next 7 days."
        )
        return
    pdf_file = export_pdf(birthdays, anniversaries)

    messagebox.showinfo(
        "Success",
        f"PDF Saved Successfully\n\n{pdf_file}"
    )

    return pdf_file
    
    