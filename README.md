# 🎮 Cartridge

A self-hosted, containerized video game collection tracker. Keep track of your physical and digital game library, rate titles, log play sessions, and visualize your collection — all from your own server.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLModel, SQLite |
| Frontend | Vue 3, Vite, Tailwind CSS, DaisyUI, Chart.js + vue-chartjs |
| Container | Docker + Docker Compose |

---

## Project Structure

```
Cartridge/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── database.py       # SQLite + SQLModel setup
│   │   ├── models.py         # Data models (Game, CollectionEntry)
│   │   ├── routers/
│   │   │   ├── games.py      # CRUD routes for games
│   │   │   └── collection.py # CRUD routes for collection entries
│   │   └── services/
│   │       └── igdb.py       # IGDB API client
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── components/
│   │   └── views/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Setup (Docker Compose)

### 1. Clone the repository

```bash
git clone https://github.com/JackJPowell/Cartridge.git
cd Cartridge
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your IGDB credentials
```

### 3. Start the application

```bash
docker compose up --build
```

- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## IGDB API Credentials

Cartridge uses the [IGDB API](https://api-docs.igdb.com/) (powered by Twitch) to fetch game metadata.

1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console/apps)
2. Log in or create a free Twitch account
3. Click **Register Your Application**
4. Set the OAuth Redirect URL to `http://localhost`
5. Copy your **Client ID** and generate a **Client Secret**
6. Add them to your `.env` file:

```env
IGDB_CLIENT_ID=your_client_id
IGDB_CLIENT_SECRET=your_client_secret
```

---

## Barcode Scanner Support

Cartridge supports USB barcode scanners out of the box. Most USB barcode scanners operate as **HID keyboard emulators** — they appear to the operating system as a keyboard and send the barcode string followed by an Enter keypress.

No drivers or special configuration are required. Simply focus the search field in the browser and scan a game's barcode; the input is captured automatically just like any keyboard input.
