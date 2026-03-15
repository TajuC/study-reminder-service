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

### Run 24/7 in the cloud (one-time setup)

1. Sign up at [fly.io](https://fly.io) and install the CLI. Run `fly auth login` (or create a token in the dashboard).
2. In your repo: **Settings → Secrets and variables → Actions**. Add:
   - `FLY_API_TOKEN` — from `fly auth token`
   - `DISCORD_WEBHOOK_URL` — your Discord webhook URL  
   Optionally add `FLY_APP_NAME` if the default name is taken (e.g. `my-study-reminder`).
3. Push to `main` or run the **Deploy to Fly.io** workflow manually. The app will be deployed and run 24/7. Each push to `main` redeploys automatically.

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

### הרצה 24/7 בענן (הגדרה חד־פעמית)

1. הירשם ב־[fly.io](https://fly.io) והתקן את ה-CLI. הרץ `fly auth login` (או צור token בדשבורד).
2. ב־**Settings → Secrets and variables → Actions** הוסף: `FLY_API_TOKEN` (מ־`fly auth token`), `DISCORD_WEBHOOK_URL` (כתובת ה-webhook). אופציונלי: `FLY_APP_NAME` אם השם כבר תפוס.
3. דחיפה ל־`main` או הרצת workflow **Deploy to Fly.io** תעלה את האפליקציה ל־24/7. כל דחיפה ל־`main` תעדכן אוטומטית.

### דרישות

Python 3.12+. נדרשים `requests`, `python-dotenv` ו-`tzdata` (לתמיכה באזור זמן ב-Windows).
