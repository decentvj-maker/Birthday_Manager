
import pandas as pd
from tkinter import Toplevel, ttk, messagebox
import customtkinter as ctk


def search_member_window(excel_file):

    if excel_file == "":
        messagebox.showwarning(
            "Warning",
            "Please Select Excel File First"
        )
        return

    win = Toplevel()

    win.title("Search Member")

    win.geometry("850x700")

    ctk.CTkLabel(
        win,
        text="Search Member",
        font=("Arial",22,"bold")
    ).pack(pady=15)

    search_entry = ctk.CTkEntry(
        win,
        width=350,
        placeholder_text="Enter Member Name"
    )

    search_entry.pack(pady=10)

    tree = ttk.Treeview(

        win,

        columns=(
            "Name",
            "Mobile",
            "Birthday",
            "Anniversary"
        ),

        show="headings",

        height=14

    )

    tree.heading("Name", text="Name")
    tree.heading("Mobile", text="Mobile")
    tree.heading("Birthday", text="Birthday")
    tree.heading("Anniversary", text="Anniversary")

    tree.column("Name", width=250)
    tree.column("Mobile", width=140)
    tree.column("Birthday", width=120)
    tree.column("Anniversary", width=120)

    tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    def search():

        for item in tree.get_children():
            tree.delete(item)

        keyword = search_entry.get().strip().lower()

        try:

            df = pd.read_excel(excel_file)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return

        df.columns = df.columns.str.strip()

        found = False

        for _, row in df.iterrows():

            name = str(row["NAME"])

            if keyword in name.lower():

                found = True

                tree.insert(

                    "",

                    "end",

                    values=(

                        row["NAME"],

                        row["MOBILE NUMBER"],

                        row["BIRTHDAY DATE"],

                        row["ANNIVERSARY DATE"]

                    )

                )

        if not found:

            messagebox.showinfo(

                "Search",

                "Member Not Found."

            )

    ctk.CTkButton(

        win,

        text="Search",

        width=180,

        command=search

    ).pack(
        pady=10
    )
        # =====================================
    # EDIT SELECTED
    # =====================================

    def edit_selected():

        selected = tree.focus()

        if selected == "":
            messagebox.showwarning(
                "Warning",
                "Please select a member."
            )
            return

        values = tree.item(selected)["values"]

        edit = Toplevel(win)

        edit.title("Edit Member")

        edit.geometry("400x420")

        ctk.CTkLabel(
            edit,
            text="Edit Member",
            font=("Arial",20,"bold")
        ).pack(pady=10)

        ctk.CTkLabel(edit,text="Name").pack()

        entry_name = ctk.CTkEntry(edit,width=250)
        entry_name.pack(pady=5)
        entry_name.insert(0, values[0])

        ctk.CTkLabel(edit,text="Mobile").pack()

        entry_mobile = ctk.CTkEntry(edit,width=250)
        entry_mobile.pack(pady=5)
        entry_mobile.insert(0, values[1])

        ctk.CTkLabel(edit,text="Birthday").pack()

        entry_birthday = ctk.CTkEntry(edit,width=250)
        entry_birthday.pack(pady=5)
        entry_birthday.insert(0,str(values[2]))

        ctk.CTkLabel(edit,text="Anniversary").pack()

        entry_anniversary = ctk.CTkEntry(edit,width=250)
        entry_anniversary.pack(pady=5)
        entry_anniversary.insert(0,str(values[3]))

        def update_member():

            df = pd.read_excel(excel_file)

            df.columns = df.columns.str.strip()

            for i in df.index:

                if str(df.loc[i,"MOBILE NUMBER"]) == str(values[1]):

                    df.loc[i,"NAME"] = entry_name.get()

                    df.loc[i,"MOBILE NUMBER"] = entry_mobile.get()

                    df.loc[i,"BIRTHDAY DATE"] = entry_birthday.get()

                    df.loc[i,"ANNIVERSARY DATE"] = entry_anniversary.get()

                    break

            df.to_excel(
                excel_file,
                index=False
            )

            messagebox.showinfo(
                "Success",
                "Member Updated Successfully."
            )

            edit.destroy()

            search()

        ctk.CTkButton(
            edit,
            text="Update",
            command=update_member
        ).pack(pady=20)

    # =====================================
    # DELETE MEMBER
    # =====================================

    def delete_selected():

        selected = tree.focus()

        if selected == "":
            messagebox.showwarning(
                "Warning",
                "Please select a member."
            )
            return

        values = tree.item(selected)["values"]

        answer = messagebox.askyesno(
            "Delete",
            f"Delete {values[0]} ?"
        )

        if not answer:
            return

        df = pd.read_excel(excel_file)

        df.columns = df.columns.str.strip()

        df = df[
            df["MOBILE NUMBER"].astype(str)
            != str(values[1])
        ]

        df.to_excel(
            excel_file,
            index=False
        )

        messagebox.showinfo(
            "Deleted",
            "Member Deleted Successfully."
        )

        search()

    button_frame = ctk.CTkFrame(win)

    button_frame.pack(pady=10)

    ctk.CTkButton(
        button_frame,
        text="Edit Selected",
        command=edit_selected
    ).pack(
        side="left",
        padx=10
    )

    ctk.CTkButton(
        button_frame,
        text="Delete Selected",
        command=delete_selected
    ).pack(
        side="left",
        padx=10
    )