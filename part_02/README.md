# YouTube Metadata Application

Part 02 contains a FastAPI backend and a Next.js frontend. The frontend accepts a YouTube URL and calls the backend to retrieve the video's title, duration, view count, and upload date.

## Requirements

- Python 3.13 or newer
- Bun 1.2.21 or newer
- A working internet connection for `yt-dlp` to query YouTube

## Backend setup

Open a terminal in `part_02/backend` and create a virtual environment:

```bash
cd part_02/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Start the API:

```bash
fastapi dev main.py --host 127.0.0.1 --port 8000
```

The backend is available at `http://127.0.0.1:8000`. Keep this terminal running while using the frontend.

### Test the backend directly

With the backend running, send a YouTube URL to the extraction endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/videos/extract \
	-H 'Content-Type: application/json' \
	-d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

The response contains JSON fields for `title`, `duration`, `view_count`, and `upload_date`.

## Frontend setup

Open a second terminal in `part_02/frontend`:

```bash
cd part_02/frontend
bun install
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser and paste a YouTube video URL into the form.

The frontend proxy uses this backend URL by default:

```text
http://127.0.0.1:8000/api/v1/videos/extract
```

To use a different backend URL, set `VIDEO_API_URL` before starting the frontend:

```bash
VIDEO_API_URL=http://127.0.0.1:8000/api/v1/videos/extract bun run dev
```

## Useful commands

Run frontend linting:

```bash
cd part_02/frontend
bun run lint
```

Create a production frontend build:

```bash
cd part_02/frontend
bun run build
bun run start
```

## Troubleshooting

- **Could not connect to the video service:** make sure the backend is running on port 8000 and that `VIDEO_API_URL` points to the correct endpoint.
- **The backend cannot fetch a video:** verify that the URL is a public YouTube video URL and that the machine has internet access.
- **Port already in use:** start the backend or frontend on another port and update `VIDEO_API_URL` if the backend port changes.

## Project structure

```text
part_02/
├── backend/
│   ├── main.py
│   └── pyproject.toml
├── frontend/
│   ├── app/
│   │   ├── api/video-info/route.ts
│   │   └── page.tsx
│   ├── package.json
│   └── tsconfig.json
└── README.md
```
