"""
Central runner for the Resume automation.

"""

from src.sites.naukri_apply_recommended import open_home_and_click_view_all
from src.utils.run_keyword_extraction import main as run_keyword_extraction
from src.sites.naukri_resume_upload import upload_resume_if_needed


def run_pipeline():
    print("\n=== STEP 1: Keyword Extraction ===")
    run_keyword_extraction()

    print("\n=== STEP 2: Conditional Resume Upload ===")
    upload_resume_if_needed()

    print("\n=== STEP 3: Open Naukri & View Recommended Jobs ===")
    open_home_and_click_view_all()

    print("\n=== PIPELINE PAUSED AT BLOCK 2 ===")
    print("No job selection or apply is performed.\n")


if __name__ == "__main__":
    run_pipeline()
