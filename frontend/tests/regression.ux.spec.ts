import { expect, test } from "@playwright/test";

test("render dashboard with multi-domain controls", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByTestId("feed-dashboard")).toBeVisible();
  await expect(page.getByTestId("domain-tab-all")).toBeVisible();
  await expect(page.getByTestId("domain-tab-crypto")).toBeVisible();
  await expect(page.getByTestId("domain-tab-ai_ml")).toBeVisible();
  await expect(page.getByTestId("topic-card").first()).toBeVisible();
  await expect(page.getByTestId("event-calendar")).toBeVisible();
});

test("domain tab filtering keeps only selected domain items", async ({ page }) => {
  await page.goto("/");

  await page.getByTestId("domain-tab-ai_ml").click();
  await page.waitForTimeout(500);
  await expect(page.getByTestId("feed-item").first()).toHaveAttribute("data-domain", "ai_ml");
  await expect(page.locator('[data-testid=\"feed-item\"][data-domain=\"crypto\"]')).toHaveCount(0, { timeout: 10000 });
});
