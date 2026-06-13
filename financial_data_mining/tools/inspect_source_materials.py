import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def inspect_assignments():
    for path in sorted((ROOT / "Assignments").glob("*.ipynb")):
        data = json.loads(path.read_text(encoding="utf-8"))
        print(f"\n### {path.name} | cells={len(data.get('cells', []))}")
        for index, cell in enumerate(data.get("cells", [])):
            source = "".join(cell.get("source", []))
            print(f"\n--- CELL {index} [{cell.get('cell_type')}] ---")
            if "data:image" in source:
                source = source.split("data:image", 1)[0] + "[embedded image omitted]"
            print(source[:8000])


def inspect_pdf_support():
    print("\n### PDF libraries")
    for name in ("pypdf", "PyPDF2", "fitz", "pdfplumber"):
        print(name, bool(importlib.util.find_spec(name)))


def extract_pdf(source_name, output_name):
    from pypdf import PdfReader

    source = ROOT / "Slides" / source_name
    output = ROOT / "Slides" / output_name
    reader = PdfReader(str(source))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        pages.append(f"--- PAGE {page_number} ---\n{page.extract_text() or ''}")
    output.write_text("\n".join(pages), encoding="utf-8")
    print(f"\nExtracted {len(reader.pages)} pages to {output}")


if __name__ == "__main__":
    inspect_assignments()
    inspect_pdf_support()
    for source_name, output_name in (
        ("chapter7_8.pdf", "chapter7_8.txt"),
        ("chapter9_10.pdf", "chapter9_10.txt"),
        ("chapter11_13.pdf", "chapter11_13.txt"),
    ):
        extract_pdf(source_name, output_name)
