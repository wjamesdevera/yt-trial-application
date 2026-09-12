type VideoInfoRequest = {
  url?: string;
};

type ExternalVideoInfo = {
  title?: string;
  duration?: number;
  view_count?: number;
  upload_date?: string;
};

function isYouTubeUrl(value: unknown): value is string {
  if (typeof value !== "string") return false;

  try {
    const url = new URL(value);
    return [
      "youtube.com",
      "www.youtube.com",
      "m.youtube.com",
      "youtu.be",
    ].includes(url.hostname.toLowerCase());
  } catch {
    return false;
  }
}

function formatDate(dateStr: string | undefined): string {
  if (dateStr === undefined || dateStr.length !== 8) {
    return "Unknown";
  }
  // Extract year, month, and day using slice
  const year = dateStr.slice(0, 4);
  const month = dateStr.slice(4, 6);
  const day = dateStr.slice(6, 8);

  return `${year}-${month}-${day}`;
}

export async function POST(request: Request) {
  let body: VideoInfoRequest;

  try {
    body = await request.json();
  } catch {
    return Response.json(
      { error: "Request body must be valid JSON." },
      { status: 400 },
    );
  }

  if (!isYouTubeUrl(body.url)) {
    return Response.json(
      { error: "Please enter a valid YouTube URL." },
      { status: 400 },
    );
  }

  const externalApiUrl =
    process.env.VIDEO_API_URL ?? "http://127.0.0.1:8000/api/v1/videos/extract";

  try {
    const externalResponse = await fetch(externalApiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: body.url }),
      signal: AbortSignal.timeout(15_000),
      cache: "no-store",
    });
    const responseBody: unknown = await externalResponse.json();

    if (!externalResponse.ok) {
      return Response.json(
        { error: "The video service could not fetch that video." },
        { status: 502 },
      );
    }

    const externalData = getExternalVideoInfo(responseBody);
    if (!externalData?.title) {
      return Response.json(
        { error: "The video service returned an unexpected response." },
        { status: 502 },
      );
    }

    return Response.json({
      title: String(externalData.title),
      duration: formatDuration(externalData.duration),
      views: formatViews(externalData.view_count),
      uploadDate: formatDate(externalData.upload_date),
    });
  } catch {
    return Response.json(
      { error: "Could not connect to the video service." },
      { status: 502 },
    );
  }
}

function getExternalVideoInfo(responseBody: unknown): ExternalVideoInfo | null {
  if (!responseBody || typeof responseBody !== "object") return null;

  const body = responseBody as Record<string, unknown>;
  const data = body.data ?? body.video ?? body;

  return data && typeof data === "object" ? (data as ExternalVideoInfo) : null;
}

function formatDuration(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value !== "number" || !Number.isFinite(value)) return "Unknown";

  const totalSeconds = Math.max(0, Math.floor(value));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  return hours > 0
    ? `${hours}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`
    : `${minutes}:${String(seconds).padStart(2, "0")}`;
}

function formatViews(value: unknown): string {
  if (typeof value === "number") return value.toLocaleString("en-US");
  return value == null ? "Unknown" : String(value);
}
