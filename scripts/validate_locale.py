import os
import sys
import re

DEFAULT_PROMPTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'prompts')
)
MAX_LENGTH = 600

def validate_locales(prompts_dir: str = DEFAULT_PROMPTS_DIR) -> list:
    """Validate locale files under prompts_dir.

    Returns a list of validation error messages.
    """
    lang_codes = [d for d in os.listdir(prompts_dir)
                  if os.path.isdir(os.path.join(prompts_dir, d))]
    # Build the reference file list from the English directory
    master_dir = os.path.join(prompts_dir, 'en')
    master_files = set()
    for root, _, files in os.walk(master_dir):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), master_dir)
            master_files.add(rel_path)

    errors = []

    for lang in lang_codes:
        lang_dir = os.path.join(prompts_dir, lang)
        file_set = set()
        for root, _, files in os.walk(lang_dir):
            for f in files:
                rel_path = os.path.relpath(os.path.join(root, f), lang_dir)
                file_set.add(rel_path)

        # Skip structure check for 'multi' directory
        if lang != 'multi' and file_set != master_files:
            diff = file_set.symmetric_difference(master_files)
            for missing_file in sorted(master_files - file_set):
                norm_missing = missing_file.replace('\\', '/')
                errors.append(
                    f"[Structure] Language '{lang}' is missing file: {norm_missing}"
                )
            for extra_file in sorted(file_set - master_files):
                norm_extra = extra_file.replace('\\', '/')
                errors.append(
                    f"[Structure] Language '{lang}' has extra file: {norm_extra}"
                )

        # Check each file for length and trailing whitespace
        for fname in file_set:
            path = os.path.join(lang_dir, fname)
            if not os.path.isfile(path):
                continue
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            length = len(content.rstrip('\n'))
            if length > MAX_LENGTH:
                errors.append(
                    f"[Length] {lang}/{fname} is {length} chars (max {MAX_LENGTH}).")
            if re.search(r"[ \t]+$", content, re.MULTILINE):
                errors.append(f"[Formatting] Trailing whitespace in {lang}/{fname}.")

    # Also validate files directly under prompts_dir (not in language subfolders)
    top_level_files = [f for f in os.listdir(prompts_dir)
                       if os.path.isfile(os.path.join(prompts_dir, f))]
    for fname in top_level_files:
        path = os.path.join(prompts_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        length = len(content.rstrip('\n'))
        if length > MAX_LENGTH:
            errors.append(
                f"[Length] {fname} is {length} chars (max {MAX_LENGTH}).")
        if re.search(r"[ \t]+$", content, re.MULTILINE):
            errors.append(f"[Formatting] Trailing whitespace in {fname}.")

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
