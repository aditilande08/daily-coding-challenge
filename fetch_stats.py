import sys
import json
import re
import requests

def get_leetcode_stats(username):
    url = 'https://leetcode.com/graphql'
    query = """
    query userProblemsSolved($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    try:
        r = requests.post(url, json={'query': query, 'variables': {'username': username}}, timeout=10)
        data = r.json()
        stats = data['data']['matchedUser']['submitStats']['acSubmissionNum']
        
        result = {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}
        for item in stats:
            diff = item['difficulty'].lower()
            if diff in result:
                result[diff] = item['count']
        result['total'] = result['easy'] + result['medium'] + result['hard']
        return result
    except Exception as e:
        print(f"Error fetching LeetCode stats: {e}", file=sys.stderr)
        return None

def get_codechef_stats(username):
    url = f"https://www.codechef.com/users/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"CodeChef page returned status code {r.status_code}", file=sys.stderr)
            return None
        
        # Look for "Total Problems Solved: XXX"
        html = r.text
        solved_match = re.search(r'Total Problems Solved:\s*(\d+)', html, re.IGNORECASE)
        total_solved = 0
        if solved_match:
            total_solved = int(solved_match.group(1))
        else:
            # Fallback search for count in text
            solved_match_alt = re.search(r'Fully Solved\s*\((\d+)\)', html, re.IGNORECASE)
            if solved_match_alt:
                total_solved = int(solved_match_alt.group(1))
                
        return {'total': total_solved}
    except Exception as e:
        print(f"Error fetching CodeChef stats: {e}", file=sys.stderr)
        return None

def main():
    lc_user = "aditilande08"
    cc_user = "gaze_doves_04"
    
    print(f"Fetching LeetCode stats for '{lc_user}'...")
    lc_stats = get_leetcode_stats(lc_user)
    
    print(f"Fetching CodeChef stats for '{cc_user}'...")
    cc_stats = get_codechef_stats(cc_user)
    
    stats_data = {
        'leetcode': lc_stats or {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0},
        'codechef': cc_stats or {'total': 0},
        'usernames': {
            'leetcode': lc_user,
            'codechef': cc_user
        }
    }
    
    # Save to stats.json
    with open('stats.json', 'w') as f:
        json.dump(stats_data, f, indent=4)
        
    # Save to stats.js to avoid browser CORS issues
    with open('stats.js', 'w') as f:
        f.write(f"window.codestreak_fetched_stats = {json.dumps(stats_data, indent=4)};\n")
        
    print("\n--- Summary ---")
    print(f"LeetCode: {stats_data['leetcode']}")
    print(f"CodeChef: {stats_data['codechef']}")
    print("Saved to stats.json successfully!")

if __name__ == '__main__':
    main()
