import { test, expect } from "@playwright/test";
import { beforeEachHook, t } from "./utils";
import "../localStorageMock";

test.describe("Portfolio", () => {

  test.beforeEach(async ({page}) => beforeEachHook(page)());

  test.beforeEach(async ({page}) => {
    await page.getByTestId("app-icon").click();
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(3).click();
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(4).click();
  });

  test("Should be able to select structure from list", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("structures.assets"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await page.getByTestId("structure-categories-structure-select").click();
    await page.getByRole("option", { name: "Structure 1" }).click();
    expect(await table.locator("tbody tr").all()).toHaveLength(3);
  });

  test("Should be possible to set structure as current", async ({ page }) => {
    const button = page.getByTestId("structure-categories-set-as-current-button");
    expect(button).toBeDisabled();

    await page.getByTestId("structure-categories-structure-select").click();
    await page.getByRole("option", { name: "Structure 1" }).click();

    await page.waitForTimeout(500);

    expect(button).toBeEnabled();
    await button.click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("structure-categories-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.structure_now_is_current"));

  });

});
