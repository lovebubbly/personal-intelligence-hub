import { expect, test } from "@playwright/test";

test("mobile nav and content visible", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("link", { name: "Feed" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Digest" })).toBeVisible();
  await expect(page.getByRole("link", { name: "KOLs" })).toBeVisible();
  await expect(page.getByTestId("feed-item").first()).toBeVisible();
});

test("mobile kols domain tabs visible", async ({ page }) => {
  await page.goto("/kols");

  await expect(page.getByTestId("kols-domain-all")).toBeVisible();
  await expect(page.getByTestId("kols-domain-crypto")).toBeVisible();
  await expect(page.getByTestId("kols-domain-ai_ml")).toBeVisible();
  await expect(page.getByTestId("kol-heatmap")).toBeVisible();
});
