import { expect, test } from "@playwright/test";

test("motion preset exposed and feed list visible", async ({ page }) => {
  await page.goto("/");

  const preset = page.getByTestId("feed-dashboard");
  await expect(preset).toHaveAttribute("data-motion-preset", /insertDuration/);
  await expect(page.getByTestId("feed-list")).toBeVisible();
});

test("digest domain switch tabs render", async ({ page }) => {
  await page.goto("/digest");

  await expect(page.getByTestId("digest-domain-crypto")).toBeVisible();
  await expect(page.getByTestId("digest-domain-ai_ml")).toBeVisible();
  await expect(page.getByTestId("digest-view")).toBeVisible();
});
