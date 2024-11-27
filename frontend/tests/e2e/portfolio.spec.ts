import { test, expect } from "@playwright/test";
import { beforeEachHook, t } from "./utils";
import "../localStorageMock";

test.describe("Portfolio", () => {

  test.beforeEach(async ({page}) => beforeEachHook(page)());

  test.beforeEach(async ({page}) => {
    await page.getByTestId("app-icon").click();
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(0).click();
  });

  test("Should show warning icon on significant difference", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("portfolio.title"));

    expect(await table.locator(".mdi-alert").all()).toHaveLength(2);

    await page.getByTestId("app-configure").click();
    const input = page.getByTestId("text-field-portfolio-diff_warning")
      .getByLabel(t("portfolio.diff_warning"));
    await input.click();
    await input.fill("8");
    await page.getByTestId("form-dialog-save-button").click();

    expect(await table.locator(".mdi-alert").all()).toHaveLength(1);

    expect(await table.locator("tbody tr").first().locator("td").nth(2).innerHTML()).toContain("mdi-alert");
  });

  test("Should be possible to do calculations", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("portfolio.title"));

    expect(await table.locator("tbody tr").first().locator("td").all()).toHaveLength(4);

    const input = page.getByTestId("portfolio-page-summa-input").locator("input");
    await input.click();
    await input.fill("1000");
    await page.getByTestId("portfolio-page-calculate-button").click();
    expect(await table.locator("tbody tr").first().locator("td").all()).toHaveLength(5);

    await page.getByTestId("portfolio-page-reset-button").click();
    expect(await table.locator("tbody tr").first().locator("td").all()).toHaveLength(4);
  });

});
