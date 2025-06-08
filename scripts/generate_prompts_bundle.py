# generate_prompts_bundle.py
import os
import re
import json

def extract_start_word(text):
    """Find the first Markdown bold phrase (e.g. **Start**) and return the inner word."""
    m = re.search(r"\*\*(.*?)\*\*", text)
    return m.group(1) if m else ""

def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def main():
    # Fix: prompts is at project root, not inside scripts
    project_root = os.path.dirname(os.path.dirname(__file__))
    prompts_dir = os.path.join(project_root, 'prompts')
    bundle = {}

    # List all subdirectories in prompts/ (skip non-directories)
    for lang in os.listdir(prompts_dir):
        lang_dir = os.path.join(prompts_dir, lang)
        if not os.path.isdir(lang_dir):
            continue

        # Read greeting and extract start word
        greeting_path = os.path.join(lang_dir, 'greeting.md')
        if not os.path.isfile(greeting_path):
            continue  # skip if missing
        greeting = load_text(greeting_path)
        start_word = extract_start_word(greeting)

        # Read the 4 questions
        questions = []
        for i in range(1, 5):
            q_path = os.path.join(lang_dir, f"q{i}_phq.md")
            if os.path.isfile(q_path):
                questions.append(load_text(q_path))

        # Read the 3 response templates
        responses = {}
        resp_dir = os.path.join(lang_dir, 'responses')
        for color in ['green', 'yellow', 'red']:
            file_name = f"score_{color}.md"
            resp_path = os.path.join(resp_dir, file_name)
            if os.path.isfile(resp_path):
                responses[color] = load_text(resp_path)

        # Add to bundle if all parts are present
        if greeting and questions and responses:
            bundle[lang] = {
                "greeting": greeting,
                "questions": questions,
                "responses": responses,
                "start_word": start_word
            }

    # Write the JSON file
    with open('prompts_bundle.json', 'w', encoding='utf-8') as outfile:
        json.dump(bundle, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
