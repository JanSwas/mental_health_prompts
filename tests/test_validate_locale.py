import os
import shutil
import importlib.util

import pytest

MODULE_PATH = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'validate_locale.py')
spec = importlib.util.spec_from_file_location('validate_locale', MODULE_PATH)
validate_locale = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_locale)


def setup_prompts(tmpdir):
    src = os.path.join(os.path.dirname(__file__), '..', 'prompts')
    dest = os.path.join(tmpdir, 'prompts')
    shutil.copytree(src, dest)
    return dest


def test_validate_locale_handles_directories(tmp_path):
    prompts_dir = setup_prompts(tmp_path)

    # Add a directory that previously caused a crash
    languages = [d for d in os.listdir(prompts_dir) if os.path.isdir(os.path.join(prompts_dir, d))]
    for lang in languages:
        os.makedirs(os.path.join(prompts_dir, lang, 'extra_dir'))

    # Old logic without an os.path.isfile check would raise IsADirectoryError (or PermissionError on Windows)
    def old_validate():
        for lang in languages:
            lang_dir = os.path.join(prompts_dir, lang)
            for fname in os.listdir(lang_dir):
                path = os.path.join(lang_dir, fname)
                with open(path, 'r', encoding='utf-8'):
                    pass

    import errno
    import sys
    expected_errors = (IsADirectoryError,)
    if sys.platform.startswith('win'):
        expected_errors = (IsADirectoryError, PermissionError)

    with pytest.raises(expected_errors):
        old_validate()

    # The current implementation should succeed without errors
    errors = validate_locale.validate_locales(prompts_dir=prompts_dir)
    assert errors == []


def test_missing_subdirectory_file_detected(tmp_path):
    prompts_dir = setup_prompts(tmp_path)

    os.remove(os.path.join(prompts_dir, 'hi', 'responses', 'score_green.md'))

    errors = validate_locale.validate_locales(prompts_dir=prompts_dir)
    assert any('responses/score_green.md' in e for e in errors)


def test_trailing_whitespace_detected(tmp_path):
    prompts_dir = setup_prompts(tmp_path)

    file_path = os.path.join(prompts_dir, 'hi', 'greeting.md')
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write('  ')

    errors = validate_locale.validate_locales(prompts_dir=prompts_dir)
    assert any('Trailing whitespace' in e for e in errors)


def test_default_prompts_dir_absolute():
    assert os.path.isabs(validate_locale.DEFAULT_PROMPTS_DIR)

