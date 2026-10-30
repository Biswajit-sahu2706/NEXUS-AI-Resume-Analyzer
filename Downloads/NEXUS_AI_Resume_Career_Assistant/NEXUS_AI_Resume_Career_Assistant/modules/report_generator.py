from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from xml.sax.saxutils import escape


def create_pdf_report(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    styles = getSampleStyleSheet()
    story = []
    for line in report_text.splitlines():
        if not line.strip():
            story.append(Spacer(1, 7))
        elif line.isupper() and len(line) < 90:
            story.append(Paragraph(f"<b>{escape(line)}</b>", styles["Heading2"]))
            story.append(Spacer(1, 4))
        else:
            story.append(Paragraph(escape(line), styles["BodyText"]))
            story.append(Spacer(1, 3))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
