import type { NextConfig } from "next";

const API_URL = process.env.API_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  // Development: the browser talks only to Next.js, which forwards /api/* to FastAPI.
  // Same origin = no CORS and simple cookies. In production the reverse proxy (Traefik) does this.
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${API_URL}/api/:path*` }];
  },
};

export default nextConfig;
