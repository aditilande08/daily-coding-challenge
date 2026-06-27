import os
import sys
import argparse
import base64
import re
from datetime import datetime
import subprocess

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '_', text).strip('_')

def get_extension(lang):
    extensions = {
        'py': 'py',
        'cpp': 'cpp',
        'java': 'java',
        'js': 'js',
        'md': 'md'
    }
    return extensions.get(lang, 'txt')

def get_comment_chars(lang):
    if lang in ['py']:
        return '# ', ' #'
    elif lang in ['md']:
        return '<!-- ', ' -->'
    else:
        return '// ', ' //'

def update_readme(platform, difficulty, title, url, filepath):
    readme_path = 'README.md'
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Header format
    header = """# Daily Coding Challenges & Learning Tracker ⚡

A repository tracking my daily problem solving and notes. Built with [CodeStreak](index.html).

## 📊 Summary Statistics
- **LeetCode**: {leetcode_count}
- **CodeChef**: {codechef_count}
- **GeeksforGeeks**: {gfg_count}
- **HackerRank**: {hr_count}
- **Today I Learned (TIL)**: {til_count}

## 🏆 Activity Log

| Date | Platform | Title | Difficulty / Topic | Solution / Note Link |
|------|----------|-------|--------------------|----------------------|
"""
    
    # Read existing entries
    entries = []
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'\| (\d{4}-\d{2}-\d{2}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| \[Link\]\(([^)]+)\) \|', content)
            for m in matches:
                entries.append({
                    'date': m[0].strip(),
                    'platform': m[1].strip(),
                    'title': m[2].strip(),
                    'difficulty': m[3].strip(),
                    'filepath': m[4].strip()
                })
    
    # Add new entry
    clean_title = f"[{title}]({url})" if url and url.startswith('http') else title
    new_entry = {
        'date': date_str,
        'platform': platform.capitalize() if platform != 'til' else 'TIL',
        'title': clean_title,
        'difficulty': difficulty.capitalize(),
        'filepath': filepath.replace('\\', '/')
    }
    
    # Avoid duplicate titles on same date
    if not any(e['title'] == new_entry['title'] and e['date'] == new_entry['date'] for e in entries):
        entries.insert(0, new_entry) # Insert at top
        
    # Recalculate counts
    counts = {'leetcode': 0, 'codechef': 0, 'geeksforgeeks': 0, 'hackerrank': 0, 'til': 0}
    for e in entries:
        plat_lower = e['platform'].lower()
        if plat_lower in counts:
            counts[plat_lower] += 1
            
    header_filled = header.format(
        leetcode_count=counts['leetcode'],
        codechef_count=counts['codechef'],
        gfg_count=counts['geeksforgeeks'],
        hr_count=counts['hackerrank'],
        til_count=counts['til']
    )
    
    # Generate table rows
    table_rows = []
    for e in entries:
        table_rows.append(f"| {e['date']} | {e['platform']} | {e['title']} | {e['difficulty']} | [Link]({e['filepath']}) |")
        
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(header_filled + '\n'.join(table_rows))

def run_git(file_path):
    try:
        # Check if it's a git repo
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            print("Initialized local Git repository.")
            
        subprocess.run(['git', 'add', file_path, 'README.md'], check=True)
        commit_msg = f"Solve/Note: {file_path.split(os.sep)[-1]}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print(f"\n[SUCCESS] Successfully committed {file_path} to your local repository!")
        print("💡 Run 'git push' to push this commit to your GitHub profile and light up your contribution graph!")
    except Exception as e:
        print(f"[ERROR] Failed to run Git commands: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Sync challenges to your git repo.")
    parser.add_argument('--title', required=True, help="Title of the coding challenge or TIL topic")
    parser.add_argument('--platform', required=True, help="leetcode, codechef, geeksforgeeks, hackerrank, til")
    parser.add_argument('--url', required=True, help="URL to the challenge page or N/A")
    parser.add_argument('--difficulty', required=True, help="easy, medium, hard or topic category")
    parser.add_argument('--lang', required=True, help="py, cpp, java, js, md")
    parser.add_argument('--code', required=True, help="Base64 encoded source code")
    
    args = parser.parse_args()
    
    # Decode code
    try:
        decoded_bytes = base64.b64decode(args.code)
        source_code = decoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 code: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Setup target paths
    if args.platform.lower() == 'til':
        target_dir = 'til'
        filename = f"{slugify(args.title)}.md"
        full_path = os.path.join(target_dir, filename)
    else:
        platform_dir = slugify(args.platform)
        diff_dir = slugify(args.difficulty)
        target_dir = os.path.join('solutions', platform_dir, diff_dir)
        file_ext = get_extension(args.lang)
        filename = f"{slugify(args.title)}.{file_ext}"
        full_path = os.path.join(target_dir, filename)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Prep comments
    c_start, c_end = get_comment_chars(args.lang if args.platform.lower() != 'til' else 'md')
    
    file_content = f"""{c_start}Platform: {args.platform.upper()}
{c_start}Topic/Problem: {args.title}
{c_start}Difficulty/Category: {args.difficulty.capitalize()}
{c_start}Link/Reference: {args.url}
{c_start}Date Solved/Logged: {datetime.now().strftime('%Y-%m-%d')}
{c_end if args.platform.lower() == 'til' else ''}
""" + source_code
    
    # Write solution file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    print(f"Created file: {full_path}")
    
    # Update README
    update_readme(args.platform, args.difficulty, args.title, args.url, full_path)
    print("Updated README.md table.")
    
    # Run git commit
    run_git(full_path)

if __name__ == '__main__':
    main()
