# pyright: reportMissingTypeStubs=false
from weasyprint import HTML
import sys

try:
    _ = HTML(string="<h1>Hello</h1>").write_pdf()  # pyright: ignore[reportUnknownMemberType]
    print("WeasyPrint works!")
except Exception as e:
    print(f"WeasyPrint failed: {e}")
    sys.exit(1)
