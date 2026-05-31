
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(summary, output_path):
    pdf = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    content = [
        Paragraph(
            "Notes Summary",
            styles["Title"]
        ),
        Spacer(1, 12),
        Paragraph(
            summary.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    ]
    pdf.build(content)