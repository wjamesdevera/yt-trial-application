# Youtube developer Technical Trial Task

## Instructions

Full-Stack Developer — Manos Corp

**Time Budget:** about 2 hours. Don't over-engineer this — we want to see how you think, not a polished product.
**Goal:** Build a tiny end-to-end feature that touches both our TypeScript and Python stack.

### Part 1 — Python (45 min)

Write a Python script that:

1. Takes a YouTube video URL as input
2. Uses yt-dlp to pull basic metadata (title, duration, view count, upload date)
3. Outputs the result as clean JSON

> Bonus (optional): Save the JSON to a local file instead of just printing it.

### Part 2 — Next.js / TypeScript (60 min)

Build a minimal Next.js page that:

1. Has a single input field for a YouTube URL and a "Fetch" button
2. Calls an API route (/api/video-info) that runs (or simulates calling) the Python script's logic
3. Displays the returned metadata (title, duration, views, upload date) on the page
4. Basic styling with Tailwind — doesn't need to be pretty, just clean

> If wiring Next.js directly to Python is awkward in your setup, it's fine to mock the API route with hardcoded/sample data and just document how you'd connect it to the real Python script in production.

### Part 3 — Short Write-Up (15 min)

In a few sentences, tell us:

1. What AI coding tool (if any) you used for this task, and roughly how — what you prompted for vs. what you wrote/fixed yourself
2. What you'd do differently if this were a real production feature (error handling, caching, rate limits, etc.)
3. Anything that broke or didn't work as expected, and how you'd debug it further with more time

Submission
Share a GitHub repo (public or invite link) or a zip with your code, plus your write-up. Reply in your Discord ticket with the link.
