from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_report(rows_uploaded,
    missing_values,
    report_path):

    c = canvas.Canvas(report_path,
        pagesize = letter)

    c.setFont("Helvetica", 12)

    c.drawString(50,
        750,
        "Data upload metrics")

    c.drawString(50,
        700,
        "Upload date: {}".\
        format(datetime.now().\
        strftime('%Y-%m-%d %H:%M:%S')))

    c.drawString(50,
        650,
        "Number of Rows Uploaded: {}".\
        format(rows_uploaded))

    c.drawString(50,
        600,
        "Number of Missing Values: {}".\
        format(missing_values))

    c.showPage()
    c.save()

    print("""File has been
        saved succesfully""",
        report_path)

report_path = "dataset_upload_report.pdf"

create_report(rows_uploaded = 1000,
    missing_values = 50,
    report_path = report_path)