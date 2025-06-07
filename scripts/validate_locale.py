import os
import sys
import re

DEFAULT_PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')
MAX_LENGTH = 600


def validate_locales(prompts_dir: str = DEFAULT_PROMPTS_DIR) -> list:
    """Validate locale files under prompts_dir.

    Returns a list of validation error messages.
    """
    lang_codes = [d for d in os.listdir(prompts_dir)
                  if os.path.isdir(os.path.join(prompts_dir, d))]
    master_files = set(os.listdir(os.path.join(prompts_dir, 'en')))

    errors = []

    for lang in lang_codes:
        lang_dir = os.path.join(prompts_dir, lang)
        entries = set(os.listdir(lang_dir))
        files = {f for f in entries if os.path.isfile(os.path.join(lang_dir, f))}

        if entries != master_files:
            diff = entries.symmetric_difference(master_files)
            errors.append(f"[Structure] Language '{lang}' has files {diff} missing or extra.")

        for fname in files:
            path = os.path.join(lang_dir, fname)
            if not os.path.isfile(path):
                continue
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            length = len(content)
            if length > MAX_LENGTH:
                errors.append(
                    f"[Length] {lang}/{fname} is {length} chars (max {MAX_LENGTH}).")
            if re.search(r"[ \t]+$", content, re.MULTILINE):
                errors.append(f"[Formatting] Trailing whitespace in {lang}/{fname}.")

    return errors


if __name__ == '__main__':
    errs = validate_locales()
    if errs:
        print("Validation failed with the following issues:")
        for e in errs:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("All locale files validated successfully.")
        sys.exit(0)
