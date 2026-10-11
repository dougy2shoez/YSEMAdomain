import os
import json
import shutil
from datetime import datetime

# === CONFIG ===
ROOT = r"C:\Users\dougy\Documents\buchi\YSEMAdomain"
POSTS_DIR = os.path.join(ROOT, "blog", "posts")
INDEX_FILE = os.path.join(POSTS_DIR, "index.json")

def load_index():
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

def format_title_date(dt):
    day = dt.day

    # English ordinal suffix
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    month = dt.strftime("%B")  # Full month name
    year = dt.year

    return f"{year} {month} {day}{suffix}"

def main():
    src_folder = input("Enter folder containing the new post: ").strip()

    if not os.path.isdir(src_folder):
        print("Folder does not exist.")
        return

    # Generate ID: YYMMDD-HHMM
    now = datetime.now()
    post_id = now.strftime("%y%m%d-%H%M")

    # Create destination folder
    dest_folder = os.path.join(POSTS_DIR, post_id)
    os.makedirs(dest_folder, exist_ok=True)

    # Find markdown file
    md_file = None
    for f in os.listdir(src_folder):
        if f.lower().endswith(".md"):
            md_file = f
            break

    if not md_file:
        print("No .md file found in folder.")
        return

    # Copy all files
    for f in os.listdir(src_folder):
        shutil.copy(os.path.join(src_folder, f), dest_folder)

    # Rename markdown file to match ID
    old_md_path = os.path.join(dest_folder, md_file)
    new_md_path = os.path.join(dest_folder, f"{post_id}.md")
    os.rename(old_md_path, new_md_path)

    # Update index.json
    index = load_index()
    index.append({
        "id": post_id,
        "title": format_title_date(now),
        "date": now.isoformat()
    })
    save_index(index)

    print(f"Post created: {post_id}")
    print(f"Files moved to: {dest_folder}")
    print("index.json updated.")

if __name__ == "__main__":
    main()
