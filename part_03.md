### What AI coding tool (if any) you used for this task, and roughly how — what you prompted for vs. what you wrote/fixed yourself

**Answer:**

```
I used GitHub Copilot in VS Code to build a lightweight frontend UI for inputting video links and displaying returned results. I also used it to draft the README.md to save time on basic documentation.

Everything else was written and integrated manually:

    Part 1 (Metadata Scraping): I wrote the core script using yt-dlp and click, referencing the official documentation to extract and structure only the metadata required by the prompt.

    Part 2 (API Integration): I built the FastAPI backend endpoints, established the frontend-to-backend connection, fetched data from the endpoint, and formatted the payload into a readable structure for the user.

My general approach is to leverage AI for boilerplate or straightforward tasks that don't require heavy custom configuration, saving my time for core business logic. I then test and refine all AI-generated output to ensure it strictly meets the task requirements.
```

### What you'd do differently if this were a real production feature (error handling, caching, rate limits, etc.)

**Answer:**

```
If this were moving to production, I would make several structural and reliability improvements:

    Input Validation & Guardrails: Enforce strict URL regex validation and handle edge cases (e.g., private videos, deleted content, invalid URLs, unavailable region locks) on both the client and server.

    Caching Layer: Implement Redis to cache metadata results by YouTube Video ID. Since YouTube video metadata changes infrequently, this avoids duplicate extraction calls and reduces latency.

    Rate Limiting & Queueing: Add IP/user-based rate limiting to prevent abuse. Because yt-dlp extraction is I/O intensive and subject to IP blocks or throttle limits from YouTube, heavy requests should be offloaded to an asynchronous task queue (like Celery or Redis Tasks) rather than processed synchronously.

    Structured Logging & Observability: Replace basic print/CLI logs with structured JSON logging to monitor extraction failure rates and track response latencies.
```

### Anything that broke or didn't work as expected, and how you'd debug it further with more time

**Answer:**

```
During initial testing, parsing edge-case metadata streams (like live streams or age-restricted videos) caused occasional extraction failures or schema mismatches in the response.

Given more time to debug and refine, I would:

    Inspect CLI stack traces and yt-dlp error logs to pinpoint where the response schema breaks.

    Implement a robust try-except wrapper with custom fallback models (using Pydantic) to handle missing or non-standard metadata fields cleanly.

    Add comprehensive unit and integration tests with mocked yt-dlp fixtures to cover edge-case payloads without making live network requests during CI/CD runs.
```
