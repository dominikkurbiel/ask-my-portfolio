import type { ReadinessResponse } from "@/lib/api/generated/model";

export type StatusTone = "ok" | "warning" | "error" | "pending";

export interface StatusView {
  tone: StatusTone;
  label: string;
}

/** Turns the readiness check (or its absence) into what the UI shows. */
export function describeReadiness(
  readiness: ReadinessResponse | undefined,
  { isPending, isError }: { isPending: boolean; isError: boolean },
): StatusView {
  if (isPending) return { tone: "pending", label: "checking…" };
  if (isError || !readiness) return { tone: "error", label: "API offline" };
  if (readiness.status === "ok") return { tone: "ok", label: "online" };
  if (!readiness.database) return { tone: "warning", label: "database unavailable" };
  return { tone: "warning", label: "pgvector missing (run migrations)" };
}
