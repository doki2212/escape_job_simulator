from pathlib import Path
from src.core.browser import PlaywrightSession, get_config

NAUKRI_STORAGE = Path("storage/naukri.json")


def smoke_test() -> None:
    config = get_config(storage_state_path=str(NAUKRI_STORAGE))

    session = PlaywrightSession(config)
    page = session.__enter__()
    try:
        page.goto("https://www.naukri.com/")
        input("If you appear logged in, press Enter to close... ")
    finally:
        session.__exit__(None, None, None)


if __name__ == "__main__":
    smoke_test()
