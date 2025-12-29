# Resume-Based Job Application Automation (Playwright + Python)

## Planned Additions
- Application checkbox selection on Naukri (bulk select & apply)
- Support for additional job portals (Indeed, Hirect)
- Keyword-based job filtering before application
- Controlled user-intervention during application questionnaires

---

## Overview

This project is a **Python + Playwright automation framework** designed to streamline parts of the job application workflow while keeping the user in control.

The automation focuses on:
- Resume-driven logic (keywords & freshness checks)
- Manual login with session reuse (no credentials stored)
- Safe, step-by-step browser automation
- Human-in-the-loop design for sensitive actions

The project intentionally avoids full hands-free automation for job applications to reduce the risk of account restrictions and to comply with real-world portal constraints.

---

## Key Features Implemented

### 1. Manual Login with Session Persistence
- Login is performed **manually** in the browser.
- Playwright `storage_state` is used to reuse sessions.
- No usernames, passwords, or OTPs are stored in code.

### 2. Resume Freshness Check
- Resume upload is triggered **only if the PDF was modified in the last 7 days**.
- Prevents unnecessary uploads and repeated portal interactions.

### 3. Resume Upload Automation (Naukri)
- Automatically navigates to the profile section.
- Uploads resume only when the freshness condition is met.
- Requires no OS-level file dialogs.

### 4. Resume Keyword Extraction
- Extracts text from the resume PDF.
- Matches it against a user-defined `keywords.txt`.
- Outputs a human-readable report:
  - `resume_keywords_found.txt`
- Enables smarter job filtering logic later.

### 5. Recommended Jobs Navigation (Naukri)
- Opens the Naukri home page using a saved session.
- Navigates to **Recommended jobs for you → View all**.
- Designed in modular blocks for easy extension.

### 6. Central Orchestration Script
- A single runner script executes all completed steps in order.
- Makes the project easy to run, pause, and resume during development.

---

## Project Structure

src/
├── core/
│   └── browser.py
│       Playwright setup and session handling
│
├── sites/
│   ├── naukri_open_home.py
│   │   Open Naukri and navigate to Recommended Jobs
│   ├── naukri_resume_upload.py
│   │   Conditional resume upload logic
│   └── naukri_setup_login.py
│       One-time manual login and session save
│
├── utils/
│   ├── keyword_extractor.py
│   │   Resume text extraction and keyword matching
│   ├── resume_check.py
│   │   Resume freshness check logic
│   └── run_keyword_extraction.py
│
└── run_all.py
    Central pipeline runner
---

## How It Works (High Level)

1. Extract keywords from the resume and generate a report.
2. Check whether the resume was updated recently.
3. Upload the resume only if needed.
4. Open Naukri and navigate to recommended jobs.
5. Pause execution for user review and control.

Each step is intentionally isolated to:
- simplify debugging
- reduce automation brittleness
- allow partial execution

---

## Technologies Used

- Python 3
- Playwright (Python)
- pdfplumber (PDF text extraction)
- dotenv (environment configuration)

---

## Security & Privacy Considerations

- **No credentials are stored** in the codebase.
- Browser session data is stored locally and **must not be committed**.
- `.env`, `storage/`, resumes, and reports are excluded via `.gitignore`.

This project is safe to share publicly as long as ignored files remain excluded.

---

## Disclaimer

This project is intended for **educational and personal automation purposes only**.

Job portals frequently change their UI and policies.  
Use responsibly and always comply with the terms of service of the respective platforms.

---

## Future Scope

- Keyword-weighted job scoring
- Bulk checkbox-based job selection
- Apply flow with user-assisted question handling
- Multi-site support with shared logic

---

## Author

Built as a learning and portfolio project to explore:
- real-world browser automation
- automation architecture
- controlled human-in-the-loop workflows




