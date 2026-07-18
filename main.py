import webbrowser
from member_manager import add_member_window
from whatsapp_sender import send_all_whatsapp
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from report import generate_weekly_report
from print_report import print_pdf

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Birthday & Anniversary Manager")
app.geometry("900x600")

excel_file = ""


# ---------------- Select File ----------------

def select_file():
    global excel_file

    file = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls *.xlsm")]
    )

    if file:
        excel_file = file
        lbl_file.configure(text=os.path.basename(file))
    else:
        lbl_file.configure(text="No File Selected")


# ---------------- Generate Report ----------------

def generate_report():

    if excel_file == "":
        messagebox.showwarning(
            "Warning",
            "Please Select Excel File"
        )
        return

    generate_weekly_report(excel_file)


# ---------------- Heading ----------------

title = ctk.CTkLabel(
    app,
    text="Birthday & Anniversary Manager",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# ---------------- File Frame ----------------

frame = ctk.CTkFrame(app)

frame.pack(fill="x", padx=20, pady=20)

btn_file = ctk.CTkButton(
    frame,
    text="Select Excel File",
    command=select_file,
    width=180
)

btn_file.pack(side="left", padx=20, pady=20)

lbl_file = ctk.CTkLabel(
    frame,
    text="No File Selected",
    font=("Arial", 15)
)

def print_report():

    if excel_file == "":
        messagebox.showwarning(
            "Warning",
            "Please Select Excel File"
        )
        return

    pdf_file = generate_weekly_report(excel_file)

    if pdf_file:
        print_pdf(pdf_file)


def whatsapp_report():

    try:
        send_all_whatsapp(excel_file)
    except Exception as e:
        print(e)
        messagebox.showerror("Error", str(e))        
        return

    send_all_whatsapp(excel_file)
def add_member():

    if excel_file == "":
        messagebox.showwarning(
            "Warning",
            "Please Select Excel File"
        )
        return

    add_member_window(excel_file)

# ---------------- Buttons ----------------

btn_generate = ctk.CTkButton(
    app,
    text="Generate Weekly Report",
    width=250,
    height=40,
    command=generate_report
)
btn_generate.pack(pady=10)


btn_print = ctk.CTkButton(
    app,
    text="Print Report",
    width=250,
    height=40,
    command=print_report
)
btn_print.pack(pady=10)


btn_pdf = ctk.CTkButton(
    app,
    text="Export PDF",
    width=250,
    height=40,
    command=generate_report
)
btn_pdf.pack(pady=10)

btn_add = ctk.CTkButton(
    app,
    text="Add Member",
    width=250,
    height=40,
    command=add_member
)

btn_add.pack(pady=10)
btn_whatsapp = ctk.CTkButton(
    app,
    text="WhatsApp",
    width=250,
    height=40,
    command=whatsapp_report
)
btn_whatsapp.pack(pady=10)


app.mainloop()