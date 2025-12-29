import os
from pathlib import Path
from dotenv import load_dotenv

from src.utils.keyword_extractor import (
    extract_text_from_pdf,
    load_keywords,
    match_keywords,
    write_keyword_report
)

load_dotenv()


def main():
    resume_path = Path(os.getenv("RESUME_PATH"))

    resume_dir = resume_path.parent
    keyword_file = resume_dir / "keywords.txt"
    output_file = resume_dir / "resume_keywords_found.txt"

    print("Resume:", resume_path)
    print("Keywords:", keyword_file)
    print("Output:", output_file)

    resume_text = extract_text_from_pdf(resume_path)
    keywords = load_keywords(keyword_file)

    found, missing = match_keywords(resume_text, keywords)

    write_keyword_report(output_file, found, missing)

    print("\n Keyword extraction completed")
    print(f"Found: {len(found)}")
    print(f"Missing: {len(missing)}")


if __name__ == "__main__":
    main()
