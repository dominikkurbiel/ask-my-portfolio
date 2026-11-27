import { ApiStatus } from "@/features/status/api-status";

export default function HomePage() {
  return (
    <main className="home">
      <h1>Ask my portfolio</h1>
      <p>An AI assistant that answers questions about my work, with sources. Work in progress.</p>
      <ApiStatus />
    </main>
  );
}
