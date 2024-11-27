import { test, expect } from "@playwright/test";
import { beforeEachHook, t } from "./utils";
import "../localStorageMock";

test.describe("Settings", () => {

  test.beforeEach(async ({page}) => beforeEachHook(page)());

  test.beforeEach(async ({page}) => {
    await page.getByTestId("app-icon").click();
  });

  test("Should show and save global settings", async ({ page }) => {
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(9).click();
    const input = page.getByTestId("text-field-settings-currency-symbol-title")
      .getByLabel(t("settings.currency.symbol.title"));
    await input.click();
    await input.fill("€");
    await page.getByTestId("form-dialog-save-button").click();

    expect(await page.locator("[data-testid$='data-table']").textContent()).toContain("€");
  });

  test("Should show and save page settings", async ({ page }) => {
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(1).click();
    expect(await page.locator("[data-testid$='data-table'] th").all()).toHaveLength(3);

    await page.getByTestId("app-configure").click();
    for (const item of ["assets.prev", "categories.1", "classes.1"]) {
      const text = t(item);
      await page.getByTestId(`switch-${item}`).getByText(text).click();
    }
    await page.getByTestId("form-dialog-save-button").click();
    expect(await page.locator("[data-testid$='data-table'] th").all()).toHaveLength(6);
  });

  test("Should be possible to drag and drop columns", async ({ page }) => {
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(1).click();
    const headers = page.locator("[data-testid$='data-table'] th");

    expect(await headers.first().textContent()).toBe(t("assets.1"));

    await page.getByTestId("app-configure").click();
    const itemTo = page.locator('div[data-draggable="true"]', { has: page.locator("[data-testid='switch-assets.1']") });
    await page.locator('div[data-draggable="true"]', { has: page.locator("[data-testid='switch-assets.amount']") })
      .dragTo(itemTo);
    await page.getByTestId("form-dialog-save-button").click();

    await page.waitForTimeout(500);

    expect(await headers.first().textContent()).toBe(t("assets.amount"));
  });

});
