# Architecture

## Runtime

The application is a Python Streamlit app. `app.py` renders the interface and calls the database and analytics modules. Streamlit reruns the script when a user changes a control or submits a form.

All app dates and emotion timestamps use India Standard Time (UTC+05:30), independent of the hosting server's timezone.

The app can use either:

- **Local SQLite** when Cloudflare D1 credentials are not all configured. The database file is `habit_tracker.db`.
- **Cloudflare D1** when `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and `D1_DATABASE_ID` are all configured. The app accesses D1 through the Cloudflare REST API, so the Python host needs outbound HTTPS access to `api.cloudflare.com`.

## Modules

- `app.py`: Daily habit entry, habit analysis, emotion logging, and emotion analysis views.
- `auth.py`: Email normalization and salted PBKDF2 password hashing and verification.
- `config.py`: User names, habit definitions, emotion choices, and database configuration.
- `database.py`: SQLite and D1 persistence operations.
- `utils.py`: Date-period filtering and habit analytics calculations.
- `tests/`: Emotion tests, mock habit data initialization, and database inspection utility.

## Data Model

### `habit_entries`

One row per user and date. The `(username, entry_date)` uniqueness constraint supports updating that day's habits. Habit values are stored as JSON in `habits_data`.

### `emotion_entries`

One row per emotion occurrence. Each row stores a username, timestamp, emotion name, intensity from 1 to 10, and an optional cause note. Multiple occurrences of the same emotion can be recorded on the same day.

### `password_users`

One row per email/password account. Each row stores a unique email, display name, salted password hash, and random internal `username` key. Habit and emotion rows are scoped by that internal key; passwords are never stored in plaintext.

Local SQLite creates the tables on startup. Cloudflare D1 tables are provisioned manually; the required SQL is in [README.md](README.md). A previous Google-auth `users` table, if present, is no longer used and is not deleted.

## Data Flows

- Habit entry: form values -> `save_entry` -> upsert by username and date -> period filter -> dashboard metrics and charts.
- Emotion entry: selected emotion, intensity, and cause -> `save_emotion_entry` -> insert timestamped occurrence -> period filter -> grouped occurrence and average-intensity analysis.

## Deployment and Access

Streamlit requires a Python runtime and cannot run directly on Cloudflare Workers. Deploy the app to Streamlit Community Cloud or another Python-capable host. Cloudflare D1 can remain the database when the host can reach the Cloudflare API and the D1 schema and credentials are configured.

Email/password sign-in is required. Passwords are hashed with PBKDF2-HMAC-SHA256 and a unique random salt. The authenticated session's internal username scopes all habit and emotion operations; the UI does not allow choosing another account's records. Email verification, password reset, and persistent login throttling are not implemented yet.
