import { test, expect } from "@playwright/test";
import { beforeEachHook, t } from "./utils";
import "../localStorageMock";

test.describe("Dictionary operations", () => {

  test.beforeEach(async ({page}) => beforeEachHook(page)());

  test.beforeEach(async ({page}) => {
    await page.getByTestId("app-icon").click();
    await page.getByTestId("app-menu").getByText(t("dictionaries")).click();
    await page.getByTestId("app-menu").locator("div.v-list-item--link").nth(7).click();
    await page.waitForTimeout(500);
  });

  test("Should be possible to filter rows", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    const input = page.getByTestId("dictionary-page-search-input").locator("input");
    await input.click();
    await input.fill("Test3");
    expect(await table.locator("tbody tr").all()).toHaveLength(2);
  });

  test("Should be possible to add item", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await page.getByTestId("dictionary-page-add-button").click();
    expect(await page.getByTestId("form-dialog-save-button")).toBeVisible();

    const input = page.getByTestId("text-field-classes-1")
      .getByLabel(t("classes.1"));
    await input.click();

    await input.fill("Test");
    expect(await page.getByTestId("form-dialog-save-button")).toBeEnabled();

    await input.fill("");
    expect(await page.getByTestId("form-dialog-save-button")).toBeDisabled();

    await input.fill("New Test");
    await page.getByTestId("form-dialog-save-button").click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("dictionary-page-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.added"));

    expect(await table.locator("tbody tr").all()).toHaveLength(5);

    expect(await table.locator("tbody tr").last().textContent()).toContain("New Test");
  });

  test("Should be impossible to add item with the same name", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await page.getByTestId("dictionary-page-add-button").click();

    const input = page.getByTestId("text-field-classes-1")
      .getByLabel(t("classes.1"));
    await input.click();
    await input.fill("Test");
    await page.getByTestId("form-dialog-save-button").click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("dictionary-page-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.backend.UNIQUE_constraint_failed"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);
  });

  test("Should be possible to delete item", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await table.locator("tbody tr").last().locator(".mdi-delete").click();
    expect(await page.getByTestId("delete-confirmation-dialog-delete-button")).toBeVisible();

    const input = page.getByTestId("delete-confirmation-dialog-input").locator("input");
    await input.click();

    await input.fill("test");
    expect(await page.getByTestId("delete-confirmation-dialog-delete-button")).toBeDisabled();

    await input.fill("delete");
    expect(await page.getByTestId("delete-confirmation-dialog-delete-button")).toBeEnabled();

    await page.getByTestId("delete-confirmation-dialog-delete-button").click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("dictionary-page-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.deleted"));

    expect(await table.locator("tbody tr").all()).toHaveLength(3);
  });

  test("Should be impossible to delete item used in other tables", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await table.locator("tbody tr").first().locator(".mdi-delete").click();
    expect(await page.getByTestId("delete-confirmation-dialog-delete-button")).toBeVisible();

    const input = page.getByTestId("delete-confirmation-dialog-input").locator("input");
    await input.click();
    await input.fill("delete");
    await page.getByTestId("delete-confirmation-dialog-delete-button").click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("dictionary-page-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.backend.FOREIGN_KEY_constraint_failed"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);
  });

  test("Should be possible to update item", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await table.locator("tbody tr").first().locator(".mdi-pencil").click();
    expect(await page.getByTestId("form-dialog-save-button")).toBeVisible();

    const input = page.getByTestId("text-field-classes-1")
      .getByLabel(t("classes.1"));

    expect(await input.inputValue()).toBe("Test");

    await input.click();
    await input.fill("Updated Test");
    await page.getByTestId("form-dialog-save-button").click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("dictionary-page-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.updated"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    expect(await table.locator("tbody tr").first().textContent()).toContain("Updated Test");
  });

  test("Should be impossible to update name to name of exists item", async ({ page }) => {
    const table = page.locator("[data-testid$='data-table']");

    expect(await table.locator(".v-toolbar-title__placeholder").textContent()).toContain(t("classes.title"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    await table.locator("tbody tr").last().locator(".mdi-pencil").click();
    expect(await page.getByTestId("form-dialog-save-button")).toBeVisible();

    const input = page.getByTestId("text-field-classes-1")
      .getByLabel(t("classes.1"));

    await input.click();
    await input.fill("Test2");
    await page.getByTestId("form-dialog-save-button").click();

    await page.waitForTimeout(500);

    const info = page.getByTestId("dictionary-page-snackbar");
    expect(await info).toBeVisible();
    expect(await info.textContent()).toContain(t("messages.backend.UNIQUE_constraint_failed"));

    expect(await table.locator("tbody tr").all()).toHaveLength(4);

    expect(await table.locator("tbody tr").last().textContent()).toContain("Test33");
  });

});
