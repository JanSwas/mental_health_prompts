Mental Health Prompts for Mental Health Screening

Open-source library of **multilingual** WhatsApp chat prompts for lightweight mental-health triage (PHQ‑4 / GAD‑2 flows) in India.

📖 Overview

This repository provides:

Standardized conversation prompts (greeting, questions, responses) for mental-health screening via WhatsApp Business App or API.

Translation-ready Markdown files, organized by language code.

A consistent flow for asking 4 questions, scoring responses, and delivering tailored guidance.

🚀 Features

Greeting message to welcome users and choose language.

PHQ‑4 / GAD‑2 questions (4 total) with multiple‑choice options.

Tailored responses for Green, Yellow, and Red risk levels.

Self-help tips, helpline links, and counselor referral templates.

Multi-language support (English en/, Hindi hi/, Bengali bn/, Marathi mr/, Tamil ta/, etc.).

📂 Repository Structure

```
mental_health_prompts/
├── README.md            # This file
├── LICENSE              # Open-source license
├── prompts/
│   ├── en/              # English prompts
│   │   ├── greeting.md
│   │   ├── q1_phq.md
│   │   ├── q2_phq.md
│   │   ├── q3_phq.md
│   │   ├── q4_phq.md
│   │   └── responses/
│   │       ├── score_green.md
│   │       ├── score_yellow.md
│   │       └── score_red.md
│   ├── hi/              # Hindi translations
│   ├── bn/              # Bengali translations
│   ├── mr/              # Marathi translations
│   └── ta/              # Tamil translations
└── scripts/
    └── validate_locale.py  # (Optional) Check consistency & length limits

```

## 📦 Utility: `generate_prompts_bundle.py`

This repository now includes **`generate_prompts_bundle.py`**, a helper script that rolls every prompt file under `prompts/` into a single **`prompts_bundle.json`**.  
That JSON becomes your one-stop “knowledge” file when you upload the project to a Custom GPT, avoiding the 20-file upload ceiling.

### What the script does

| Step | Action |
|------|--------|
| 1 | Scans each sub-folder inside `prompts/` (e.g. `en/`, `hi/`, `bn/`, `mr/`, `ta/`, …). |
| 2 | Reads **`greeting.md`**, **`q1_phq.md` … `q4_phq.md`**, and all three response files under `responses/` for that language. |
| 3 | Extracts the *translated* word used for **Start** from the greeting (first `**bolded**` term). |
| 4 | Builds a dictionary of the form:<br>```json\n{\n  \"en\": {\n    \"greeting\": \"...\",\n    \"questions\": [\"...\", \"...\", \"...\", \"...\"],\n    \"responses\": {\"green\": \"...\", \"yellow\": \"...\", \"red\": \"...\"},\n    \"start_word\": \"Start\"\n  },\n  \"hi\": { ... },\n  ...\n}\n``` |
| 5 | Writes the result to **`prompts_bundle.json`** in the repo root. |

### Prerequisites

* Python 3.8 + (the script only uses the standard library).

### Usage

```bash
# 1. Clone this repo and cd into it
git clone https://github.com/JanSwas/mental_health_prompts.git
cd mental_health_prompts

# 2. Run the generator (from repo root OR inside prompts/, both work)
python generate_prompts_bundle.py

# 3. You should see:
# ✅  prompts_bundle.json created for: en, hi, bn, mr, ta

# 4. Inspect (optional)
cat prompts_bundle.json | python -m json.tool | head


🤝 Contributing

We welcome contributions from developers, translators, and mental-health professionals:

Fork this repository.

Create a new branch (git checkout -b feature/my-language).

Add or update prompt files under the appropriate prompts/<lang>/ directory.

Run validation (optional):

python scripts/validate_locale.py

Open a Pull Request, describing your changes. We’ll review and merge!

Please ensure:

Prompt files are in Markdown (*.md).

Each file is ≤ 600 characters to fit WhatsApp message limits.

Filenames & folder structure mirror the en/ directory.

⚙️ Formatting Guidelines

Use plain text and avoid emojis in core prompts (you can add them in response files sparingly).

Use backticks for placeholders (e.g., {{user_name}}).

Do not include personal data or PII.

Keep lines ≤ 80 characters for readability.

📜 License

This project is licensed under the MIT License — see LICENSE for details.

Built with ❤️ for accessible mental-health support.

