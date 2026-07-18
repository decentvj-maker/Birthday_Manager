from tkcalendar import DateEntry
import pandas as pd
from tkinter import Toplevel, messagebox
import customtkinter as ctk
from tkcalendar import DateEntry
import os


def add_member_window(excel_file):

    # Check Excel selected
    if excel_file == "":
        messagebox.showwarning(
            "Warning",
            "Please Select Excel File First"
        )
        return

    # Window
    win = Toplevel()
    win.title("Add New Member")
    win.geometry("500x700")
    win.resizable(False, False)
    

    # ---------------- Labels ----------------

    ctk.CTkLabel(
        win,
        text="Add New Member",
        font=("Arial", 22, "bold")
    ).pack(pady=15)

    # Name

    ctk.CTkLabel(
        win,
        text="Name"
    ).pack()

    entry_name = ctk.CTkEntry(
        win,
        width=300
    )
    entry_name.pack(pady=5)

    # Mobile

    ctk.CTkLabel(
        win,
        text="Mobile Number"
    ).pack()

    entry_mobile = ctk.CTkEntry(
        win,
        width=300
    )
    entry_mobile.pack(pady=5)

    # Birthday

    ctk.CTkLabel(
        win,
        text="Birthday (DD-MM-YYYY)"
    ).pack()

    birthday_entry = DateEntry(
    win,
    width=22,
    date_pattern="dd-mm-yyyy"
    )
    birthday_entry.pack(pady=5)

    # Anniversary

    ctk.CTkLabel(
        win,
        text="Anniversary (DD-MM-YYYY)"
    ).pack()

    anniversary_entry = DateEntry(
    win,
    width=22,
    date_pattern="dd-mm-yyyy"
    )
    anniversary_entry.pack(pady=5)

    # ---------------- Save ----------------

    def save_member():

        name = entry_name.get().strip()
        mobile = entry_mobile.get().strip()
        birthday = entry_birthday.get().strip()
        anniversary = entry_anniversary.get().strip()

        if name == "":
            messagebox.showerror(
                "Error",
                "Please Enter Name"
            )
            return

        if mobile == "":
            messagebox.showerror(
                "Error",
                "Please Enter Mobile Number"
            )
            return

        # Read Excel

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
            return

        df.columns = df.columns.str.strip()

        # Duplicate Mobile Check

        if "MOBILE NUMBER" in df.columns:

            mobile_list = (
                df["MOBILE NUMBER"]
                .astype(str)
                .str.strip()
                .tolist()
            )

            if mobile in mobile_list:

                messagebox.showwarning(
                    "Duplicate",
                    "Mobile Number Already Exists."
                )
                return

        # New Row

        new_row = {
            "NAME": name,
            "MOBILE NUMBER": mobile,
            "BIRTHDAY DATE": birthday,
            "ANNIVERSARY DATE": anniversary
        }

        df.loc[len(df)] = new_row

        try:
            df.to_excel(
                excel_file,
                index=False
            )

            messagebox.showinfo(
                "Success",
                "Member Added Successfully."
            )

            win.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # Save Button

    ctk.CTkButton(
        win,
        text="Save Member",
        width=200,
        command=save_member
    ).pack(pady=25)
