import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import expect

from src.core.browser import PlaywrightSession, get_config
from src.utils.resume_check import resume_modified_within_days

load_dotenv()

NAUKRI_STORAGE = Path("storage/naukri.json")
NAUKRI_PROFILE_URL = "https://www.naukri.com/mnjuser/profile"
RESUME_DAYS_THRESHOLD = 7


def upload_resume_if_needed() -> None:
    resume_path = Path(os.getenv("RESUME_PATH"))

    if not resume_modified_within_days(resume_path, RESUME_DAYS_THRESHOLD):
        print(f" Resume not modified in last {RESUME_DAYS_THRESHOLD} days.")
        print("Skipping resume upload.")
        return

    print("Resume modified recently. Proceeding with upload.")

    config = get_config(storage_state_path=str(NAUKRI_STORAGE))
    session = PlaywrightSession(config)
    page = session.__enter__()

    try:
        print("Opening Naukri profile page...")
        page.goto(NAUKRI_PROFILE_URL)

        # Wait until profile loads
        page.wait_for_load_state("networkidle")

        resume_inputs = page.locator("input[type='file']")

        # Pick the first one (resume upload)
        resume_input = resume_inputs.first

        print(f"Found {resume_inputs.count()} file inputs. Using the first one.")

        resume_input.set_input_files(str(resume_path))

        # Give Naukri time to process upload
        page.wait_for_timeout(5000)

        print("Resume upload triggered. Please visually confirm success.")
        input("Press Enter to close browser after confirmation...")

    finally:
        session.__exit__(None, None, None)


if __name__ == "__main__":
    upload_resume_if_needed()
