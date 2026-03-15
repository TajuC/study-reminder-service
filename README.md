# Study Reminder Service

Sends Discord webhook reminders for your weekly class schedule. Edit `schedule.json`, set your webhook in `.env`, and run. Works on Windows and Linux.

---

## English

### What it does

- Reads a weekly schedule from `schedule.json`
- Sends Discord messages 10 min, 5 min, 1 min before class and at start time
- Uses SQLite so it never sends the same reminder twice, even after restart
- Skips holidays via `skip_dates`; semester end is set in the JSON

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`: set `DISCORD_WEBHOOK_URL` to your Discord webhook. Edit `schedule.json` with your classes and dates.

### Run

```bash
python -m app.main
```

Set `DRY_RUN=true` in `.env` to test without sending. On Windows, use `scripts\install_windows_task.ps1` (as Administrator) to run at logon.

### Run in the cloud (100% free, no card)

Scheduled run every 5 minutes. No sign-up or payment anywhere.

1. Keep the repo **public** (Actions minutes are free for public repos).
2. In the repo: **Settings → Secrets and variables → Actions**. Add one secret: `DISCORD_WEBHOOK_URL` (your Discord webhook URL).
3. Run **Reminder check (free, every 5 min)** once from the Actions tab (or wait for the next run). It will then run automatically every 5 minutes. No duplicates: state is cached between runs. (Reminders are checked every 5 min, so they can be up to 5 minutes late.) Your PC can be off; the workflow runs on GitHub’s servers. **Note:** Scheduled runs use an offset cron (`2-59/5`) to avoid GitHub’s high load at the top of each hour; they can still be delayed. If no schedule run appears after 20+ minutes, run it once manually (Run workflow) or push a change to the workflow file to re-register the schedule.

**When does it run?** The workflow runs **every 5 minutes** on a schedule (you may see runs with event “schedule” in the Actions tab; runs from “Commit pushed” are from editing the workflow file). Each run checks the current time: **Discord messages are only sent when a reminder is actually due** (10, 5, or 1 minute before a class, or at class start). So you’ll see workflow runs in Actions every 5 min, but messages in Discord only around your class times.

**Where is "every 5 minutes" defined?** In the workflow file, the line `cron: '2-59/5 * * * *'` under `schedule:` tells **GitHub's servers** to trigger the workflow at :02, :07, :12, :17, … UTC (every 5 minutes). GitHub's scheduler does this automatically; no one has to click anything. If **schedule runs never appear** (only manual or push runs), GitHub's cron can be unreliable for some repos. **Fallback:** use a free external cron (e.g. [cron-job.org](https://cron-job.org)) to run every 5 minutes and call the GitHub API: `POST https://api.github.com/repos/OWNER/REPO/actions/workflows/reminder-cron.yml/dispatches` with header `Authorization: token YOUR_PAT` and body `{"ref":"main"}` (PAT needs permission to trigger workflows).

### Requirements

Python 3.12+. Needs `requests`, `python-dotenv`, and `tzdata` (for Windows timezone support).

---

## עברית

### מה זה עושה

- קורא מערכת שבועית מקובץ `schedule.json`
- שולח הודעות בדיסקורד 10 דקות, 5 דקות, דקה לפני השיעור ובשעת התחלה
- משתמש ב-SQLite כדי לא לשלוח אותה תזכורת פעמיים, גם אחרי הפעלה מחדש
- מדלג על חופשות דרך `skip_dates`; סוף הסמסטר מוגדר ב-JSON

### התקנה

```bash
pip install -r requirements.txt
cp .env.example .env
```

ערוך את `.env`: הגדר `DISCORD_WEBHOOK_URL` ל-webhook של הדיסקורד שלך. ערוך את `schedule.json` עם השיעורים והתאריכים.

### הרצה

```bash
python -m app.main
```

הגדר `DRY_RUN=true` ב-`.env` לבדיקה בלי שליחה. ב-Windows אפשר להריץ את `scripts\install_windows_task.ps1` (כמנהל) כדי שהשירות יעלה בהתחברות.

### הרצה בענן (חינם לגמרי, בלי כרטיס אשראי)

הרצה מתוזמנת כל 5 דקות, בלי הרשמה או תשלום.

1. השאר את ה-repo **ציבורי** (דקות Actions חינם).
2. ב־**Settings → Secrets and variables → Actions** הוסף סוד אחד: `DISCORD_WEBHOOK_URL` (כתובת ה-webhook).
3. הפעל פעם אחת את **Reminder check (free, every 5 min)** בלשונית Actions (או חכה לריצה הבאה). מהריצה הבאה זה ירוץ אוטומטית כל 5 דקות. בלי כפילויות: המצב נשמר בין ריצות. המחשב שלך יכול להיות כבוי — ה-workflow רץ על שרתי GitHub. (תדירות המינימום של GitHub היא 5 דקות, גם עם Pro/Education.)

### דרישות

Python 3.12+. נדרשים `requests`, `python-dotenv` ו-`tzdata` (לתמיכה באזור זמן ב-Windows).
