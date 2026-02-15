import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 40_000,
  fullyParallel: true,
  use: {
    baseURL: "http://127.0.0.1:3100",
    trace: "retain-on-failure"
  },
  webServer: {
    command: "NEXT_PUBLIC_USE_MOCK=true pnpm dev --port 3100",
    port: 3100,
    reuseExistingServer: false,
    timeout: 120_000
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "Mobile Safari", use: { ...devices["iPhone 13"] } }
  ]
});
