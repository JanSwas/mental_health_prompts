import os
import sys
import glob
import re

# Configuration
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')
MAX_LENGTH = 600
LANG_CODES = [d for d in os.listdir(PROMPTS_DIR) if os.path.isdir(os.path.join(PROMPTS_DIR, d))]
MASTER_FILES = set(os.listdir(os.path.join(PROMPTS_DIR, 'en')))

errors = []

for lang in LANG_CODES:
    lang_dir = os.path.join(PROMPTS_DIR, lang)
    entries = set(os.listdir(lang_dir))
    files = {f for f in entries if os.path.isfile(os.path.join(lang_dir, f))}
    subdirs = {d for d in entries if os.path.isdir(os.path.join(lang_dir, d))}
    # Check same filenames
    if entries != MASTER_FILES:
        diff = entries.symmetric_difference(MASTER_FILES)
        errors.append(f"[Structure] Language '{lang}' has files {diff} missing or extra.")
    # Check each file length
    for fname in files:
        path = os.path.join(lang_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        length = len(content)
        if length > MAX_LENGTH:
            errors.append(f"[Length] {lang}/{fname} is {length} chars (max {MAX_LENGTH}).")
        # No trailing whitespace
        if re.search(r"[ \t]+$", content, re.MULTILINE):
            errors.append(f"[Formatting] Trailing whitespace in {lang}/{fname}.")

# Report
if errors:
    print("Validation failed with the following issues:")
    for err in errors:
        print(f" - {err}")
    sys.exit(1)
else:
    print("All locale files validated successfully.")
    sys.exit(0)
