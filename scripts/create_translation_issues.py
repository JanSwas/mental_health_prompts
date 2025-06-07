"""
create_translation_issues.py

Automate the creation of GitHub issues for native speaker review of machine-generated translations in the prompts directory.

Usage:
  1. Place your GitHub personal access token in a .env or .env.local file in the project root as GITHUB_TOKEN=your_token_here (do not commit this file).
  2. Place your GitHub repository name in the .env or .env.local file as GITHUB_REPO=yourusername/mental_health_prompts.
  3. Run: python scripts/create_translation_issues.py [lang_code] [--dry-run]
     - Optionally provide a two-letter language code (e.g., 'hi') to create an issue for only that language.
     - Use --dry-run to preview the issue(s) without creating them.
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load GITHUB_TOKEN and GITHUB_REPO from .env or .env.local
env_path = Path(__file__).parent.parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    raise RuntimeError(".env or .env.local file not found in project root.")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPO")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set in .env or .env.local file.")
if not REPO:
    raise RuntimeError("GITHUB_REPO not set in .env or .env.local file.")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')

# Parse command-line arguments
lang_arg = None
is_dry_run = False
for arg in sys.argv[1:]:
    if arg.startswith('--dry-run'):
        is_dry_run = True
    elif len(arg) == 2:
        lang_arg = arg

langs = [lang_arg] if lang_arg else [d for d in os.listdir(prompts_dir) if d != "en" and os.path.isdir(os.path.join(prompts_dir, d))]

for lang in langs:
    lang_path = os.path.join(prompts_dir, lang)
    if not os.path.isdir(lang_path):
        print(f"Language directory not found: {lang_path}")
        continue

    # Check for any existing issue (open or closed) for this language
    title = f"{lang.upper()} Translation Validation Needed"
    search_url = f"https://api.github.com/search/issues"
    params = {
        "q": f'repo:{REPO} is:issue in:title "{title}"'
    }
    search_resp = requests.get(search_url, headers=headers, params=params)
    if search_resp.status_code == 200 and search_resp.json()["total_count"] > 0:
        print(f"Issue already exists for {lang}, skipping.")
        continue

    files = []
    for root, _, filenames in os.walk(lang_path):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), lang_path)
            files.append(rel_path.replace("\\", "/"))

    body = (
        f"A native {lang.upper()} speaker is needed to review and validate the machine-generated translations in the `prompts/{lang}/` directory.\n\n"
        "Please check all prompt and response files for accuracy, clarity, and cultural appropriateness.\n\n"
        "Files to review:\n"
        + "\n".join(f"- `{file}`" for file in files) +
        "\n\nPlease update any incorrect or awkward translations and open a pull request with your changes.\n\nThank you for your help!"
    )

    if is_dry_run:
        print(f"[DRY RUN] Would create issue for {lang} with title:\n{title}\nBody:\n{body}\n---")
        continue

    response = requests.post(
        f"https://api.github.com/repos/{REPO}/issues",
        headers=headers,
        json={"title": title, "body": body}
    )
    if response.status_code == 201:
        print(f"Issue created for {lang}: {response.json()['html_url']}")
    else:
        print(f"Failed to create issue for {lang}: {response.text}")
