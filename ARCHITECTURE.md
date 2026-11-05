# Architecture

## Runtime

The application is a Python Streamlit app. `app.py` renders the interface and calls the database and analytics modules. Streamlit reruns the script when a user changes a control or submits a form.

All app dates and emotion timestamps use India Standard Time (UTC+05:30), independent of the hosting server's timezone.

The app can use either:

- **Local SQLite** when Cloudflare D1 credentials are not all configured. The database file is `habit_tracker.db`.
- **Cloudflare D1** when `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and `D1_DATABASE_ID` are all configured. The app accesses D1 through the Cloudflare REST API, so the Python host needs outbound HTTPS access to `api.cloudflare.com`.

## Modules

- `app.py`: Daily habit entry, habit analysis, emotion logging, and emotion analysis views.
- `config.py`: User names, habit definitions, emotion choices, and database configuration.
- `database.py`: SQLite and D1 persistence operations.
- `utils.py`: Date-period filtering and habit analytics calculations.
- `tests/`: Emotion tests, mock habit data initialization, and database inspection utility.

## Data Model

### `habit_entries`

One row per user and date. The `(username, entry_date)` uniqueness constraint supports updating that day's habits. Habit values are stored as JSON in `habits_data`.

### `emotion_entries`

One row per emotion occurrence. Each row stores a username, timestamp, emotion name, intensity from 1 to 10, and an optional cause note. Multiple occurrences of the same emotion can be recorded on the same day.

Local SQLite creates both tables on startup. Cloudflare D1 tables are provisioned manually; the required SQL is in [README.md](README.md).

## Data Flows

- Habit entry: form values -> `save_entry` -> upsert by username and date -> period filter -> dashboard metrics and charts.
- Emotion entry: selected emotion, intensity, and cause -> `save_emotion_entry` -> insert timestamped occurrence -> period filter -> grouped occurrence and average-intensity analysis.

## Deployment and Access

Streamlit requires a Python runtime and cannot run directly on Cloudflare Workers. Deploy the app to Streamlit Community Cloud or another Python-capable host. Cloudflare D1 can remain the database when the host can reach the Cloudflare API and the D1 schema and credentials are configured.

Google OIDC sign-in is required. The authenticated email must be explicitly mapped to an existing username in the `authorized_users` Streamlit secrets table. Database operations use that mapped username; the UI does not allow choosing a different user's records. OAuth credentials and the cookie secret belong in Streamlit secrets, never in source control.
