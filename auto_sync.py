import os
import sys
import requests
import json
import re
from datetime import datetime
import subprocess

LEETCODE_USERNAME = "aditilande08"

def get_recent_accepted_submissions(username):
    url = 'https://leetcode.com/graphql'
    query = """
    query userRecentSubmissions($username: String!, $limit: Int!) {
      recentSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
        statusDisplay
        lang
      }
    }
    """
    try:
        r = requests.post(url, json={'query': query, 'variables': {'username': username, 'limit': 15}}, timeout=10)
        data = r.json()
        submissions = data['data']['recentSubmissionList']
        
        # Filter for Accepted solutions
        accepted = []
        for s in submissions:
            if s['statusDisplay'] == 'Accepted':
                accepted.append(s)
        return accepted
    except Exception as e:
        print(f"Error fetching recent submissions: {e}", file=sys.stderr)
        return []

def get_problem_details(title_slug):
    url = 'https://leetcode.com/graphql'
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        difficulty
      }
    }
    """
    try:
        r = requests.post(url, json={'query': query, 'variables': {'titleSlug': title_slug}}, timeout=10)
        data = r.json()
        return data['data']['question']
    except Exception as e:
        print(f"Error fetching problem details for {title_slug}: {e}", file=sys.stderr)
        return None

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '_', text).strip('_')

def get_extension(lang):
    extensions = {
        'python': 'py',
        'python3': 'py',
        'cpp': 'cpp',
        'java': 'java',
        'javascript': 'js',
        'typescript': 'ts'
    }
    return extensions.get(lang.lower(), 'py')

def get_comment_chars(lang):
    if lang.lower() in ['python', 'python3', 'py']:
        return '# ', ' #'
    else:
        return '// ', ' //'

def update_readme(platform, difficulty, title, url, filepath):
    readme_path = 'README.md'
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Read existing entries
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
    
    new_entry = {
        'date': date_str,
        'platform': platform.capitalize(),
        'title': f"[{title}]({url})",
        'difficulty': difficulty.capitalize(),
        'filepath': filepath.replace('\\', '/')
    }
    
    # Avoid duplicates
    if not any(e['title'] == new_entry['title'] for e in entries):
        entries.insert(0, new_entry)
        
    counts = {'leetcode': 0, 'codechef': 0, 'geeksforgeeks': 0, 'hackerrank': 0}
    for e in entries:
        plat_lower = e['platform'].lower()
        if plat_lower in counts:
            counts[plat_lower] += 1
            
    header = f"""# Daily Coding Challenges Tracker ⚡

A repository tracking my daily problem solving across various platforms. Built with [CodeStreak](index.html).

## 📊 Summary Statistics
- **LeetCode**: {counts['leetcode']}
- **CodeChef**: {counts['codechef']}
- **GeeksforGeeks**: {counts['geeksforgeeks']}
- **HackerRank**: {counts['hackerrank']}

## 🏆 Problem Log

| Date | Platform | Title | Difficulty | Solution Link |
|------|----------|-------|------------|---------------|
"""
    
    table_rows = []
    for e in entries:
        table_rows.append(f"| {e['date']} | {e['platform']} | {e['title']} | {e['difficulty']} | [Solution]({e['filepath']}) |")
        
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(header + '\n'.join(table_rows))

def auto_sync():
    print(f"Checking for recent accepted LeetCode submissions for '{LEETCODE_USERNAME}'...")
    submissions = get_recent_accepted_submissions(LEETCODE_USERNAME)
    
    if not submissions:
        print("No recent accepted submissions found or profile is set to private.")
        return
        
    new_commits = 0
    
    for sub in submissions:
        title = sub['title']
        title_slug = sub['titleSlug']
        lang = sub['lang']
        
        # Get problem details
        details = get_problem_details(title_slug)
        if not details:
            continue
            
        difficulty = details['difficulty'].lower()
        ext = get_extension(lang)
        filename = f"{slugify(title)}.{ext}"
        
        # Setup paths
        target_dir = os.path.join('solutions', 'leetcode', difficulty)
        full_path = os.path.join(target_dir, filename)
        
        # If solution already exists, skip it
        if os.path.exists(full_path):
            continue
            
        print(f"Found new solution: {title} ({details['difficulty']})")
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Create file content
        c_start, _ = get_comment_chars(lang)
        problem_url = f"https://leetcode.com/problems/{title_slug}/"
        
        file_content = f"""{c_start}Platform: LeetCode
{c_start}Problem: {title}
{c_start}Difficulty: {details['difficulty']}
{c_start}Link: {problem_url}
{c_start}Date Solved: {datetime.now().strftime('%Y-%m-%d')}

{c_start}Paste your solved code solution below:
{c_start}---
"""
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
            
        # Update README
        update_readme('leetcode', difficulty, title, problem_url, full_path)
        
        # Git commit
        try:
            subprocess.run(['git', 'add', full_path, 'README.md'], check=True)
            subprocess.run(['git', 'commit', '-m', f"Auto-sync: {title} ({details['difficulty']})"], check=True)
            new_commits += 1
            print(f"Committed new solution to repo.")
        except Exception as e:
            print(f"Git commit failed: {e}")
            
    if new_commits > 0:
        print(f"\n[SYNC COMPLETE] Created and committed {new_commits} new solutions!")
        print("Pushing to GitHub to update your green dots...")
        try:
            subprocess.run(['git', 'push'], check=True)
            print("Successfully pushed to GitHub! Check your profile!")
        except Exception as e:
            print(f"Git push failed: {e}. Please run 'git push' manually.")
    else:
        print("\nAll recent LeetCode solutions are already up-to-date! No action required.")

if __name__ == '__main__':
    auto_sync()
