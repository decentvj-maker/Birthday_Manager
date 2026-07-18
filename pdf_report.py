from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def export_pdf(birthdays, anniversaries):

    # Reports folder automatically create hoga
    os.makedirs("Reports", exist_ok=True)

    # Full path banega
    filename = os.path.abspath(
        f"Reports/Weekly_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    c = canvas.Canvas(filename, pagesize=A4)

    y = 800

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, y, "Weekly Birthday Report")

    y -= 40

    # Birthdays
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Birthdays")

    y -= 25

    c.setFont("Helvetica", 12)

    if birthdays:
        for item in birthdays:
            c.drawString(
                60,
                y,
                f"{item[0]}   {item[1]}   {item[2]}"
            )
            y -= 20
    else:
        c.drawString(60, y, "No Birthdays")
        y -= 20

    y -= 30

    # Anniversaries
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Anniversaries")

    y -= 25

    c.setFont("Helvetica", 12)

    if anniversaries:
        for item in anniversaries:
            c.drawString(
                60,
                y,
                f"{item[0]}   {item[1]}   {item[2]}"
            )
            y -= 20
    else:
        c.drawString(60, y, "No Anniversaries")

    c.save()

    return filename