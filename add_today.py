import os
import sys
import re
import subprocess
from datetime import datetime

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '_', text).strip('_')

def get_extension(lang):
    ext_map = {
        'python': 'py', 'py': 'py',
        'c++': 'cpp', 'cpp': 'cpp',
        'java': 'java',
        'javascript': 'js', 'js': 'js',
        'sql': 'sql',
        'markdown': 'md', 'md': 'md'
    }
    return ext_map.get(lang.lower(), 'py')

def get_comment_syntax(ext):
    if ext == 'py':
        return '# '
    elif ext == 'sql':
        return '-- '
    elif ext == 'md':
        return ''
    else:
        return '// '

def update_readme(platform, difficulty, title, url, filepath):
    readme_path = 'README.md'
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    entries = []
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'\| (\d{4}-\d{2}-\d{2}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| \[Solution\]\(([^)]+)\) \|', content)
            for m in matches:
                entries.append({
                    'date': m[0].strip(),
                    'platform': m[1].strip(),
                    'title': m[2].strip(),
                    'difficulty': m[3].strip(),
                    'filepath': m[4].strip()
                })
    
    title_link = f"[{title}]({url})" if url and url.startswith('http') else title
    new_entry = {
        'date': date_str,
        'platform': platform.capitalize() if platform.lower() != 'til' else 'TIL',
        'title': title_link,
        'difficulty': difficulty.capitalize(),
        'filepath': filepath.replace('\\', '/')
    }
    
    # Avoid duplicate titles on same date
    if not any(e['title'] == new_entry['title'] and e['date'] == new_entry['date'] for e in entries):
        entries.insert(0, new_entry)
        
    counts = {'leetcode': 0, 'codechef': 0, 'geeksforgeeks': 0, 'hackerrank': 0, 'til': 0}
    for e in entries:
        p = e['platform'].lower()
        if p in counts:
            counts[p] += 1
            
    header = f"""# Daily Coding Challenges Tracker ⚡

A repository tracking my daily problem solving across various platforms. Built with [CodeStreak](index.html).

## 📊 Summary Statistics
- **LeetCode**: {counts['leetcode']}
- **CodeChef**: {counts['codechef']}
- **GeeksforGeeks**: {counts['geeksforgeeks']}
- **HackerRank**: {counts['hackerrank']}
- **Today I Learned / Projects**: {counts['til']}

## 🏆 Problem Log

| Date | Platform | Title | Difficulty | Solution Link |
|------|----------|-------|------------|---------------|
"""
    table_rows = [f"| {e['date']} | {e['platform']} | {e['title']} | {e['difficulty']} | [Solution]({e['filepath']}) |" for e in entries]
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(header + '\n'.join(table_rows) + '\n')

def main():
    print("=" * 55)
    print(" 🚀 Daily Coding Challenge Streak Logger")
    print("=" * 55)
    
    # Platform
    print("\nSelect Platform:")
    print("1) LeetCode\n2) CodeChef\n3) GeeksforGeeks\n4) HackerRank\n5) TIL / Custom")
    plat_choice = input("Enter choice [1-5, default 1]: ").strip() or "1"
    plat_dict = {"1": "LeetCode", "2": "CodeChef", "3": "GeeksforGeeks", "4": "HackerRank", "5": "TIL"}
    platform = plat_dict.get(plat_choice, "LeetCode")
    
    title = input("\nProblem Title (e.g. Reverse Linked List): ").strip()
    if not title:
        print("[ERROR] Title cannot be empty.")
        return
        
    url = input("Problem URL (optional, press Enter to skip): ").strip()
    if not url:
        url = "N/A"
        
    diff = input("Difficulty [Easy / Medium / Hard, default Easy]: ").strip() or "Easy"
    lang = input("Language [py / cpp / java / js / sql, default py]: ").strip() or "py"
    ext = get_extension(lang)
    
    # Location
    plat_dir = slugify(platform)
    diff_dir = slugify(diff)
    filename = f"{slugify(title)}.{ext}"
    target_dir = os.path.join("solutions", plat_dir, diff_dir)
    os.makedirs(target_dir, exist_ok=True)
    full_path = os.path.join(target_dir, filename)
    
    comment_char = get_comment_syntax(ext)
    
    print("\nEnter/paste your code solution below. Press Ctrl+Z (Windows) and Enter when finished:")
    code_lines = sys.stdin.read()
    
    header_comment = f"""{comment_char}Platform: {platform}
{comment_char}Problem: {title}
{comment_char}Difficulty: {diff.capitalize()}
{comment_char}Link: {url}
{comment_char}Date: {datetime.now().strftime('%Y-%m-%d')}

"""
    full_file_content = header_comment + (code_lines if code_lines.strip() else f"{comment_char}Solution code\n")
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(full_file_content)
        
    print(f"\n[OK] Saved code to: {full_path}")
    
    update_readme(platform, diff, title, url, full_path)
    print("[OK] Updated README.md log table")
    
    # Git commit and push
    try:
        subprocess.run(['git', 'add', full_path, 'README.md'], check=True)
        commit_msg = f"{platform}: {title} ({diff.capitalize()})"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print(f"[OK] Created Git commit: '{commit_msg}'")
        
        push_confirm = input("\nPush to GitHub now to light up today's green square? (Y/n): ").strip().lower()
        if push_confirm in ['', 'y', 'yes']:
            print("Pushing to GitHub...")
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print("\n🎉 SUCCESS! Pushed to GitHub. Check your profile graph!")
        else:
            print("Changes committed locally. Run 'git push' whenever you are ready.")
    except Exception as e:
        print(f"[ERROR] Git operation failed: {e}")

if __name__ == '__main__':
    main()
