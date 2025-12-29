from src.core.browser import PlaywrightSession, get_config

def main():
    config = get_config()
    session = PlaywrightSession(config)
    page = session.__enter__()
    try:
        page.goto("https://www.google.com")
        input("If you see the browser, press Enter to close...")
    finally:
        session.__exit__(None, None, None)

if __name__ == "__main__":
    main()
