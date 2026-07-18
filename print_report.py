import os
import platform
import subprocess
from tkinter import messagebox


def print_pdf(pdf_file):
    try:
        if platform.system() == "Windows":
            os.startfile(pdf_file, "print")
        else:
            subprocess.run(["lp", pdf_file])

        messagebox.showinfo("Success", "Print command sent successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))