# BookingHub — Unified Booking Platform for Kyrgyzstan

BookingHub is the first unified online booking platform in Kyrgyzstan covering hotels, restaurants, events, tours, nomad experiences and local guides in a single interface.

## Live Demo
- **Frontend:** https://booking-hub-frontend-eight.vercel.app
- **Backend API:** https://bookinghub-a69i.onrender.com/api/
- **API Docs:** https://bookinghub-a69i.onrender.com/api/docs/

## Features
- Hotels, Restaurants, Events, Tours booking
- Nomad Experience packages
- Local Guides hiring
- AI Travel Assistant (Russian & Kyrgyz language)
- JWT Authentication with 3 roles (Guest, Business Owner, Admin)
- Local payment systems (Mbank, Elcart, Optima Bank)
- Multilingual interface (English, Russian, Kyrgyz)
- Interactive Leaflet.js map
- Business Owner analytics dashboard
- Docker containerization
- Sentry monitoring

## Tech Stack
- **Backend:** Django 6.0, Django REST Framework, PostgreSQL 15
- **Frontend:** Vue.js 3, Pinia, Vue Router, Tailwind CSS
- **AI:** Claude API / OpenRouter
- **Deployment:** Render (backend), Vercel (frontend)
- **Other:** Docker, Sentry, 2GIS API, JWT

## Installation

### Backend
```bash
git clone https://github.com/jasmin0105/BookingHub
cd BookingHub
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
git clone https://github.com/jasmin0105/BookingHub-frontend
cd BookingHub-frontend
npm install
npm run dev
```

## API Endpoints
Full API documentation available at `/api/docs/`

## Author
Yusupova Zhasmin, COM-22, Ala-Too International University, 2026
