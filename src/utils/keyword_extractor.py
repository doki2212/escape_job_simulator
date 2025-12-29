from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract all text from a PDF file.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"Resume not found: {pdf_path}")

    text_chunks = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    return "\n".join(text_chunks).lower()


def load_keywords(keyword_file: Path) -> list[str]:
    """
    Load keywords from keywords.txt
    """
    if not keyword_file.exists():
        raise FileNotFoundError(f"Keyword file not found: {keyword_file}")

    keywords = []
    with keyword_file.open("r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip().lower()
            if clean:
                keywords.append(clean)

    return keywords


def match_keywords(resume_text: str, keywords: list[str]) -> tuple[list[str], list[str]]:
    """
    Returns (found, missing)
    """
    found = []
    missing = []

    for kw in keywords:
        if kw in resume_text:
            found.append(kw)
        else:
            missing.append(kw)

    return found, missing


def write_keyword_report(
    output_path: Path,
    found: list[str],
    missing: list[str]
) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        f.write("FOUND KEYWORDS:\n")
        for kw in found:
            f.write(f"- {kw}\n")

        f.write("\nMISSING KEYWORDS:\n")
        for kw in missing:
            f.write(f"- {kw}\n")
