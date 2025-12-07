from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from app.models import Invoice, User

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def generate_pdf(invoice: Invoice, user: User) -> bytes:
    template = env.get_template("invoice.html")
    html_content = template.render(invoice=invoice, user=user)
    return HTML(string=html_content).write_pdf()
