"use client";

import { FormEvent, useState } from "react";

type VideoMetadata = {
  title: string;
  duration: string;
  views: string;
  uploadDate: string;
};

export default function Home() {
  const [url, setUrl] = useState("");
  const [metadata, setMetadata] = useState<VideoMetadata | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMetadata(null);
    setIsLoading(true);

    try {
      const response = await fetch("/api/video-info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? "Unable to fetch video information.");
      }

      setMetadata(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to fetch video information.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center px-6 py-16">
      <div className="mb-8">
        <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-red-600">
          Video inspector
        </p>
        <h1 className="text-4xl font-semibold tracking-tight text-slate-950">
          YouTube metadata
        </h1>
        <p className="mt-3 text-slate-600">
          Paste a video URL to retrieve its basic details.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:flex-row">
        <label htmlFor="video-url" className="sr-only">
          YouTube URL
        </label>
        <input
          id="video-url"
          type="url"
          required
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          placeholder="https://www.youtube.com/watch?v=..."
          className="min-w-0 flex-1 rounded-lg border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition focus:border-red-500 focus:ring-2 focus:ring-red-100"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-lg bg-red-600 px-6 py-3 font-medium text-white transition hover:bg-red-700 disabled:cursor-wait disabled:opacity-60"
        >
          {isLoading ? "Fetching..." : "Fetch"}
        </button>
      </form>

      {error && (
        <p
          role="alert"
          className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          {error}
        </p>
      )}

      {metadata && (
        <section
          aria-live="polite"
          className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <h2 className="text-lg font-semibold text-slate-950">
            Video details
          </h2>
          <dl className="mt-5 grid gap-5 sm:grid-cols-2">
            {(
              [
                ["Title", metadata.title],
                ["Duration", metadata.duration],
                ["Views", metadata.views],
                ["Upload date", metadata.uploadDate],
              ] as const
            ).map(([label, value]) => (
              <div key={label}>
                <dt className="text-sm text-slate-500">{label}</dt>
                <dd className="mt-1 font-medium text-slate-900">{value}</dd>
              </div>
            ))}
          </dl>
        </section>
      )}
    </main>
  );
}
