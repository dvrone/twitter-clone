# Twitter Clone

A minimal Twitter-style microblogging app built with Flask. Terminal/log-inspired dark UI, self-referential follow graph, and a like system — built step by step as a learning project.

## Features

- User registration & login (Flask-Login, hashed passwords via Werkzeug)
- Post tweets (280 char limit)
- Like / unlike tweets
- Follow / unfollow users
- Personalized feed — shows tweets from people you follow, plus your own
- User profile pages with follower/following counts
- Delete your own tweets (with ownership check)
- Dark, monospace, terminal-log-style UI (JetBrains Mono, custom CSS over Bootstrap 5.3)

## Tech Stack

- **Backend:** Python, Flask (app factory + blueprints)
- **Database:** SQLite via Flask-SQLAlchemy
- **Auth:** Flask-Login
- **Forms/CSRF:** Flask-WTF
- **Frontend:** Bootstrap 5.3.3, custom dark theme (`app/static/css/style.css`)

## Project Structure

```
twitter-clone/
├── app/
│   ├── __init__.py          # app factory, extensions
│   ├── models.py            # User, Tweet, likes/follows association tables
│   ├── forms.py             # WTForms: register, login, tweet
│   ├── routes/
│   │   ├── auth.py          # register/login/logout
│   │   └── main.py          # feed, profile, like/unlike, follow/unfollow, delete
│   ├── static/css/style.css
│   └── templates/
│       ├── base.html
│       ├── auth/
│       └── main/
├── instance/app.db           # SQLite DB (gitignored)
├── config.py
├── run.py
└── requirements.txt
```

## Setup

```bash
git clone git@github.com:dvrone/twitter-clone.git
cd twitter-clone

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python -c "from app import create_app; app = create_app(); print('OK')"

python run.py
```

Visit `http://127.0.0.1:5000` — you'll be redirected to log in, then can register a new account.

## Database

SQLite database lives at `instance/app.db` and is created automatically on first run via `db.create_all()`. Schema changes during development require deleting and recreating it:

```bash
rm instance/app.db
python -c "from app import create_app; app = create_app(); print('OK')"
```

(No Flask-Migrate yet — fine for development, but real migrations would be needed before this held production data.)

## Data Model

- **User** — auth fields, bio, joined date
- **Tweet** — body (max 280 chars), timestamp, `user_id` FK
- **likes** — association table (`user_id`, `tweet_id`) for the User↔Tweet many-to-many
- **follows** — self-referential association table (`follower_id`, `followed_id`) on User

## Known Limitations / Next Steps

- No pagination — feed loads all matching tweets at once
- No profile editing (bio is set at the model level but has no UI yet)
- `has_liked()` runs one query per tweet card (N+1) — fine at this scale, would need batching for production
- No tests yet
