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

<img width="1417" height="710" alt="Screenshot 2026-07-08 at 1 06 53 PM" src="https://github.com/user-attachments/assets/baa3a5a1-6954-4ba5-be4c-a34ab7cb3d68" />
Home Page
<br><br>

<img width="1339" height="738" alt="Screenshot 2026-07-08 at 1 11 25 PM" src="https://github.com/user-attachments/assets/5d926407-4f7c-4c46-864d-79da02d481fa" />
Search Page (not logged in)
<br><br>


<img width="1270" height="722" alt="Screenshot 2026-07-08 at 1 11 43 PM" src="https://github.com/user-attachments/assets/a9281c03-6b95-4872-91bb-d77e1e8e6066" />
Login Page
<br><br>


<img width="1325" height="736" alt="Screenshot 2026-07-08 at 1 11 57 PM" src="https://github.com/user-attachments/assets/1db98389-0d0f-4863-9717-d0b3161650cf" />
Search Page (logged in)
<br><br>


<img width="1346" height="742" alt="Screenshot 2026-07-08 at 1 12 35 PM" src="https://github.com/user-attachments/assets/616edfab-da95-405a-9ce1-03b7ec73e872" />
Example search
<br><br>


<img width="1174" height="742" alt="Screenshot 2026-07-08 at 1 37 14 PM" src="https://github.com/user-attachments/assets/a69a6f74-56ab-4bc1-943b-678d46de7c50" />
User Profile
<br><br>

<img width="722" height="595" alt="Screenshot 2026-07-08 at 1 13 28 PM" src="https://github.com/user-attachments/assets/97f79982-9caa-4104-b4f3-97672572b7b2" />
<br><br>



### TODO
- Refresh token implementation on the frontend is still in progress
- Register page is not yet functional (backend is complete)

### Deployment
- Frontend: https://trash-helper-nyc.vercel.app
- Backend: https://trashhelper-369898338593.us-east1.run.app

### Contact
- LinkedIn: https://www.linkedin.com/in/yetunde-korede
- Project Link: https://github.com/yakor26/trash-helper-nyc
