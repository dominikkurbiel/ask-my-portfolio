import { describe, expect, it } from "vitest";
import { describeReadiness } from "./describe-readiness";

const idle = { isPending: false, isError: false };

describe("describeReadiness", () => {
  it("is pending while the request is in flight", () => {
    expect(describeReadiness(undefined, { isPending: true, isError: false }).tone).toBe("pending");
  });

  it("is an error when the API cannot be reached", () => {
    expect(describeReadiness(undefined, { isPending: false, isError: true })).toEqual({
      tone: "error",
      label: "API offline",
    });
  });

  it("is ok when the database and pgvector are ready", () => {
    expect(describeReadiness({ status: "ok", database: true, pgvector: true }, idle).tone).toBe(
      "ok",
    );
  });

  it("explains which dependency is missing", () => {
    expect(
      describeReadiness({ status: "unavailable", database: false, pgvector: false }, idle).label,
    ).toBe("database unavailable");
    expect(
      describeReadiness({ status: "unavailable", database: true, pgvector: false }, idle).label,
    ).toMatch(/pgvector/);
  });
});
