from pathlib import Path
import os
import traceback

from src.core.browser import PlaywrightSession, get_config

NAUKRI_STORAGE = Path("storage/naukri.json")
NAUKRI_LOGIN_URL = "https://www.naukri.com/nlogin/login"


def setup_naukri_login() -> None:
    print("\n=== DEBUG INFO ===")
    print("Current working directory:", Path.cwd())
    print("Will save storage to:", NAUKRI_STORAGE.resolve())
    print("Storage folder exists?:", NAUKRI_STORAGE.parent.exists())
    print("==================\n")

    config = get_config(storage_state_path=None)

    session = PlaywrightSession(config)
    page = session.__enter__()
    try:
        page.goto(NAUKRI_LOGIN_URL)

        print("\n=== NAUKRI LOGIN SETUP ===")
        print("1) Log in manually in the opened browser.")
        print("2) Complete OTP/captcha manually if shown.")
        print("3) After login completes, DO NOT close the browser.\n")
        input("Press Enter here AFTER login is complete to save session... ")

        # Extra debug: show what URL you're on when saving
        try:
            print("Page URL at save time:", page.url)
        except Exception:
            pass

        # Saving session
        try:
            session.save_storage_state(NAUKRI_STORAGE)
            print("\n save_storage_state() called successfully.")
        except Exception as e:
            print("\n Failed to save storage_state:", repr(e))
            print(traceback.format_exc())
            return

        print("File exists after save?:", NAUKRI_STORAGE.exists())
        print(f"Saved file path: {NAUKRI_STORAGE.resolve()}\n")

    finally:
        session.__exit__(None, None, None)


if __name__ == "__main__":
    setup_naukri_login()
