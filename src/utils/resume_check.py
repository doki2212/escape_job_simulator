from pathlib import Path
from datetime import datetime, timedelta


def resume_modified_within_days(resume_path: Path, days: int) -> bool:
    """
    Returns True if the resume file was modified within the last `days`.
    """
    if not resume_path.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")

    modified_time = datetime.fromtimestamp(resume_path.stat().st_mtime)
    cutoff_time = datetime.now() - timedelta(days=days)

    return modified_time >= cutoff_time
