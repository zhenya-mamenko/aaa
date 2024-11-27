import { test, expect } from "@playwright/test";
import { beforeEachHook, t } from "./utils";
import "../localStorageMock";

test.describe("Navigation", () => {

  test.beforeEach(async ({page}) => beforeEachHook(page)());

  test("Should be possible to use the menu", async ({ page }) => {

      const drawer = page.getByTestId("app-navigation-drawer");
      await expect(drawer).not.toBeInViewport();

      await page.getByTestId("app-icon").click();
      await expect(drawer).toBeInViewport();

  });

  test("Should be possible to navigate from the menu", async ({ page }) => {
    const menuButton = page.getByTestId("app-icon");
    const items = page.getByTestId("app-menu").locator("div.v-list-item--link");
    expect(await items.all()).toHaveLength(10);

    let toolbar;

    for (const [i, item] of ["assets.statements", "assets.state", "portfolio.title"].entries()) {
      await menuButton.click();
      await items.nth(2 - i).click();
      toolbar = page.locator("[data-testid$='data-table'] .v-toolbar-title__placeholder").textContent();
      expect(await toolbar).toContain(t(item));
    }

    await menuButton.click();
    await page.getByTestId("app-menu").getByText(t("dictionaries")).click();

    for (const [i, item] of [
      "structures.assets", "assets.title", "categories.title", "classes.title", "structures.title"
    ].entries()) {
      await items.nth(i + 4).click();
      toolbar = page.locator("[data-testid$='data-table'] .v-toolbar-title__placeholder").textContent();
      expect(await toolbar).toContain(t(item));
      await menuButton.click();
    }

  });

});
