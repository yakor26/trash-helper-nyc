# Trash Guide NYC
Trash Guide NYC is an unoffical trash guide web application that helps NYC residents manage proper trash disposal. Users can save their addresses, view their sanitation pickup schedules, and check for collection delays or suspensions, as well receives updates about delays. This not an official NYC website or in any way affiliated with DSNY.

## Overview
- Save, update, and delete multiple addresses
- View personalized sanitation schedule
- Get latest sanitation pickup alerts 
- Secure registration, login, and profile management with JWT authentication

## Tech Stack
**Frontend**
- React, TypeScript
- Chakra UI

**Backend**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- PyJWT
- NeonDB
- APScheduler

**External APIs Used**
- NYC Geoclient
- NYC 311
- TextBelt

## Getting Started
### Prerequisites
- Node.js v18+
- Python 3.12+
- PostgreSQL

### Installation
```bash
git clone https://github.com/yakor26/trash-helper-nyc.git
cd trash-helper-nyc
```

**Frontend**
```bash
cd frontend
npm install
```

**Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the `backend/` directory:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (e.g. `postgresql://user:password@localhost/dbname`) |
| `OPEN_API_GEOCLIENT_KEY` | NYC Geoclient API subscription key |
| `SECRET_KEY` | Secret key for JWT token |

### Database Setup
```bash
cd backend
alembic upgrade head
```

### Running the App
**Backend**
```bash
uvicorn app.main:app --reload
```

**Frontend**
```bash
npm run dev
```
The frontend runs on `http://localhost:5173` and the backend API on `http://localhost:8000`.

#### Usage


## TODO
- Refresh token implementation on the frontend is still in progress
- Register page is not yet functional (backend is complete)

### Deployment
- Frontend: https://trash-helper-nyc.vercel.app
- Backend: https://trashhelper-369898338593.us-east1.run.app

### Contact
- LinkedIn: https://www.linkedin.com/in/yetunde-korede
- Project Link: https://github.com/yakor26/trash-helper-nyc