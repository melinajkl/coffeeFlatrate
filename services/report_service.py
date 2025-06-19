"""
Module to generate a weekly PDF report for the CoffeeClub system.

This report includes summary statistics, top users, popular drinks, and subscription usage
for a given café over a specified week.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import date, timedelta

def generate_weekly_report_pdf():
    """
    Generates a weekly PDF report with dummy data and saves it to 'reports/weekly_report.pdf'.

    Returns:
        str: The path to the generated PDF file.
    """
    # Dummy data for example
    cafe_name = "Caffe Aroma"
    start_date = date(2025, 6, 10)
    end_date = start_date + timedelta(days=6)
    drinks_served = 238
    abo_users = 46
    top_users = [("Anna Becker", 18), ("Jonas Müller", 15), ("Lara Schmidt", 14)]
    popular_drinks = [("Cappuccino", 94), ("Flat White", 66), ("Espresso", 43)]
    abos = [("Barista Basic", 27, 120), ("Latte Lover", 14, 88), ("Caffeine Unlimited", 5, 30)]

    # File path
    os.makedirs("reports", exist_ok=True)
    pdf_path = "reports/weekly_report.pdf"

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "CoffeeClub Weekly Report")

    c.setFont("Helvetica", 12)
    y -= 30
    c.drawString(50, y, f"Café: {cafe_name}")
    y -= 20
    c.drawString(50, y, f"Week: {start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}")

    y -= 30
    c.drawString(50, y, "------------------------------------------------------------")
    y -= 20
    c.drawString(50, y, f"📊 Summary:")
    y -= 20
    c.drawString(70, y, f"- Total Drinks Served: {drinks_served}")
    y -= 20
    c.drawString(70, y, f"- Unique Aboinhaber:innen Served: {abo_users}")

    y -= 30
    c.drawString(50, y, "🏆 Top Aboinhaber:innen:")
    for name, count in top_users:
        y -= 20
        c.drawString(70, y, f"- {name} – {count} drinks")

    y -= 30
    c.drawString(50, y, "🥤 Most Popular Drinks:")
    for drink, count in popular_drinks:
        y -= 20
        c.drawString(70, y, f"- {drink}: {count}")

    y -= 30
    c.drawString(50, y, "📈 Subscription Usage:")
    for abo, users, total in abos:
        y -= 20
        c.drawString(70, y, f"- Abo \"{abo}\": {users} users ({total} drinks)")

    y -= 40
    c.drawString(50, y, "------------------------------------------------------------")
    y -= 20
    c.drawString(50, y, "Thank you for being part of CoffeeClub! ")
    y -= 20
    c.drawString(50, y, "See you next week ☕")

    c.save()
    return pdf_path
