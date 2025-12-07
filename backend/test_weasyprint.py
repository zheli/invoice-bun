from weasyprint import HTML
import sys

try:
    HTML(string="<h1>Hello</h1>").write_pdf()
    print("WeasyPrint works!")
except Exception as e:
    print(f"WeasyPrint failed: {e}")
    sys.exit(1)
