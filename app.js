// CodeStreak Tracker state and logic
document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const form = document.getElementById('challenge-form');
    const outputCard = document.getElementById('output-card');
    const syncCommandText = document.getElementById('sync-command-text');
    
    const totalSolvedEl = document.getElementById('total-solved');
    const easyCountEl = document.getElementById('easy-count');
    const mediumCountEl = document.getElementById('medium-count');
    const hardCountEl = document.getElementById('hard-count');
    
    const easyBar = document.getElementById('easy-bar');
    const mediumBar = document.getElementById('medium-bar');
    const hardBar = document.getElementById('hard-bar');
    
    const streakDaysEl = document.getElementById('streak-days');
    const streakBar = document.getElementById('streak-bar');
    const totalProgressRing = document.getElementById('total-progress-ring');
    
    // Circle progress properties
    const ringRadius = 50;
    const circumference = 2 * Math.PI * ringRadius;
    totalProgressRing.style.strokeDasharray = `${circumference} ${circumference}`;
    totalProgressRing.style.strokeDashoffset = circumference;
    
    // Load local storage data
    let stats = JSON.parse(localStorage.getItem('codestreak_stats')) || {
        easy: 0,
        medium: 0,
        hard: 0,
        streak: 0,
        lastSolvedDate: null
    };

    // Override with fetched profile stats if available
    if (window.codestreak_fetched_stats) {
        const lc = window.codestreak_fetched_stats.leetcode;
        stats.easy = lc.easy;
        stats.medium = lc.medium;
        stats.hard = lc.hard;
        
        // Dynamic stats updates
        const activePlatformItem = document.querySelector('.platform-item:nth-child(1) p');
        if (activePlatformItem) {
            activePlatformItem.innerHTML = `User: <strong>${window.codestreak_fetched_stats.usernames.leetcode}</strong><br>Solved: <strong>${lc.total}</strong> problems`;
        }
        const chefPlatformItem = document.querySelector('.platform-item:nth-child(2) p');
        if (chefPlatformItem) {
            chefPlatformItem.innerHTML = `User: <strong>${window.codestreak_fetched_stats.usernames.codechef}</strong><br>Solved: <strong>${window.codestreak_fetched_stats.codechef.total}</strong> problems`;
        }
    }

    updateUI();

    // Form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const title = document.getElementById('problem-title').value.trim();
        const platform = document.getElementById('problem-platform').value;
        const url = document.getElementById('problem-url').value.trim();
        const difficulty = document.getElementById('problem-difficulty').value;
        const language = document.getElementById('problem-language').value;
        const code = document.getElementById('solution-code').value;
        
        // Update stats
        stats[difficulty]++;
        
        // Calculate streak
        const todayStr = new Date().toDateString();
        if (stats.lastSolvedDate) {
            const lastDate = new Date(stats.lastSolvedDate);
            const diffTime = Math.abs(new Date(todayStr) - lastDate);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (diffDays === 1) {
                stats.streak++;
            } else if (diffDays > 1) {
                stats.streak = 1;
            }
        } else {
            stats.streak = 1;
        }
        stats.lastSolvedDate = todayStr;
        
        // Save stats
        localStorage.setItem('codestreak_stats', JSON.stringify(stats));
        updateUI();
        
        // Base64 encode the code to ensure safety in terminal args
        const b64Code = btoa(unescape(encodeURIComponent(code)));
        
        // Generate command
        const command = `python sync_challenge.py --title "${title}" --platform "${platform}" --url "${url}" --difficulty "${difficulty}" --lang "${language}" --code "${b64Code}"`;
        
        syncCommandText.textContent = command;
        outputCard.style.display = 'block';
        outputCard.scrollIntoView({ behavior: 'smooth' });
    });
    
    function updateUI() {
        const total = stats.easy + stats.medium + stats.hard;
        totalSolvedEl.textContent = total;
        easyCountEl.textContent = stats.easy;
        mediumCountEl.textContent = stats.medium;
        hardCountEl.textContent = stats.hard;
        
        // Calculate percentages
        const easyPct = total ? (stats.easy / total) * 100 : 0;
        const mediumPct = total ? (stats.medium / total) * 100 : 0;
        const hardPct = total ? (stats.hard / total) * 100 : 0;
        
        easyBar.style.width = `${easyPct}%`;
        mediumBar.style.width = `${mediumPct}%`;
        hardBar.style.width = `${hardPct}%`;
        
        // Streak display
        streakDaysEl.textContent = stats.streak;
        const streakPct = Math.min((stats.streak / 30) * 100, 100); // 30 day target visual
        streakBar.style.width = `${streakPct}%`;
        
        // Ring offset
        const ringOffset = circumference - (Math.min(total, 100) / 100) * circumference;
        totalProgressRing.style.strokeDashoffset = ringOffset;
    }
});

// Copy helper function
window.copyCommand = function() {
    const text = document.getElementById('sync-command-text').textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.querySelector('.btn-copy');
        btn.textContent = 'Copied!';
        setTimeout(() => {
            btn.textContent = 'Copy Command';
        }, 2000);
    });
};
