import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Page, TimeoutError as PWTimeoutError

from src.core.browser import PlaywrightSession, get_config

load_dotenv()

NAUKRI_STORAGE = Path("storage/naukri.json")
NAUKRI_HOME_URL = "https://www.naukri.com/"


def read_found_keywords_from_report() -> list[str]:
    """
    Reads resume_keywords_found.txt from the same folder as RESUME_PATH and returns only the FOUND keywords.
    Expected format:
      FOUND KEYWORDS:
      - selenium
      - playwright
      ...
      MISSING KEYWORDS:
      ...
    """
    resume_path = Path(os.getenv("RESUME_PATH"))
    report_path = resume_path.parent / "resume_keywords_found.txt"

    if not report_path.exists():
        raise FileNotFoundError(f"Keyword report not found: {report_path}")

    found: list[str] = []
    in_found_section = False

    with report_path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()

            if s.upper().startswith("FOUND KEYWORDS"):
                in_found_section = True
                continue

            if s.upper().startswith("MISSING KEYWORDS"):
                break

            if in_found_section and s.startswith("- "):
                found.append(s[2:].strip())

    return found


def click_view_all_in_recommended_widget(page: Page) -> None:
    """
    Clicks the "View all" link shown on the 'Recommended jobs for you' widget.
    Uses multiple fallback selectors.
    """
    selectors = [
        # Most direct
        "a:has-text('View all')",

        # More contextual: "View all" near the header
        "div:has-text('Recommended jobs for you') a:has-text('View all')",
        "section:has-text('Recommended jobs for you') a:has-text('View all')",

        # Text fallback
        "text=View all",
    ]

    for sel in selectors:
        try:
            loc = page.locator(sel).first
            loc.wait_for(state="visible", timeout=8000)
            loc.click(timeout=8000)
            page.wait_for_load_state("networkidle")
            print("✅ Clicked 'View all'")
            return
        except PWTimeoutError:
            continue
        except Exception:
            continue

    # If all selectors fail, pause and let user click manually once
    print("⚠️ Could not click 'View all' via selectors.")
    input("Please click 'View all' manually in the browser, then press Enter here to continue... ")
    page.wait_for_load_state("networkidle")


def open_home_and_click_view_all() -> None:
    config = get_config(storage_state_path=str(NAUKRI_STORAGE))
    session = PlaywrightSession(config)
    page: Page = session.__enter__()

    try:
        # ---- Read keywords report ----
        found_keywords = read_found_keywords_from_report()
        print(f"\n✅ Loaded FOUND keywords from report: {len(found_keywords)}")
        print(found_keywords)

        # ---- Open Naukri home ----
        print("\nOpening Naukri home page...")
        page.goto(NAUKRI_HOME_URL)
        page.wait_for_load_state("networkidle")

        # Quick sanity: if Login visible, session may be expired
        try:
            if page.locator("text=Login").first.is_visible():
                print("⚠️ Login button detected — session may be expired.")
                input("Please login manually in the browser, then press Enter here...")
                page.wait_for_load_state("networkidle")
            else:
                print("✅ Logged in (Login button not visible).")
        except Exception:
            pass

        # ---- Click "View all" in Recommended widget ----
        print("\nAttempting to click 'View all' in 'Recommended jobs for you' section...")
        click_view_all_in_recommended_widget(page)

        print("\n✅ You should now be on the full Recommended Jobs page.")
        input("Press Enter to close...")

    finally:
        session.__exit__(None, None, None)


if __name__ == "__main__":
    open_home_and_click_view_all()
