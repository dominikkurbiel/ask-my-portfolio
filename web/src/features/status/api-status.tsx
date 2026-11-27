"use client";

import { useGetReadiness } from "@/lib/api/generated/health/health";
import { describeReadiness } from "./describe-readiness";

export function ApiStatus() {
  // Generated hook: typed request + caching/refetching by TanStack Query
  const readiness = useGetReadiness({ query: { refetchInterval: 15_000 } });

  const view = describeReadiness(readiness.data?.data, {
    isPending: readiness.isPending,
    isError: readiness.isError,
  });

  return (
    <p className={`status status--${view.tone}`}>
      API: <strong>{view.label}</strong>
    </p>
  );
}
