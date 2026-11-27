import { defineConfig } from "orval";

// Generates typed fetch functions + TanStack Query hooks from the FastAPI OpenAPI schema.
// Regenerate after changing the API: (cd ../api && uv run python -m scripts.export_openapi) && pnpm api:generate
export default defineConfig({
  api: {
    input: { target: "../api/openapi.json" },
    output: {
      mode: "tags-split", // one file per OpenAPI tag (= per backend module)
      target: "src/lib/api/generated/endpoints.ts",
      schemas: "src/lib/api/generated/model",
      client: "react-query",
      httpClient: "fetch",
      clean: true,
    },
  },
});
