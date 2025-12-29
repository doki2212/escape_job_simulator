from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

load_dotenv()

@dataclass(frozen=True)
class BrowserConfig:
    headless: bool
    slow_mo_ms: int
    storage_state_path: Optional[Path] = None
    
def _env_bool(key:str, default:bool) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")

def get_config(storage_state_path: Optional[str] = None) -> BrowserConfig:
    headless = _env_bool("HEADLESS", False)
    slow_mo_ms = int(os.getenv("SLOW_MO_MS", "0"))

    ssp = Path(storage_state_path) if storage_state_path else None
    return BrowserConfig(headless=headless, slow_mo_ms=slow_mo_ms, storage_state_path=ssp)

class PlaywrightSession:
    def __init__(self, config: BrowserConfig):
        self.config = config
        self._pw = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    def __enter__(self) -> Page:
        self._pw = sync_playwright().start()

        self._browser = self._pw.chromium.launch(
            headless=self.config.headless,
            slow_mo=self.config.slow_mo_ms,
        )
        context_args = {}
        if self.config.storage_state_path and self.config.storage_state_path.exists():
            context_args["storage_state"] = str(self.config.storage_state_path)

        self._context = self._browser.new_context(**context_args)
        self._page = self._context.new_page()

        # sensible defaults
        self._page.set_default_timeout(30_000)
        self._page.set_default_navigation_timeout(45_000)

        return self._page
    
    def save_storage_state(self, path: Path) -> None:
        if not self._context:
            raise RuntimeError("Browser context not initialized.")
        path.parent.mkdir(parents=True, exist_ok=True)
        self._context.storage_state(path=str(path))

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
        finally:
            if self._pw:
                self._pw.stop()