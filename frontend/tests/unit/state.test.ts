// @ts-ignore
import { state } from "@/common/state";


describe("State", () => {

  test("Currency position", () => {
    state.settings.global.currency[1].value = [
      { value: "after", selected: false },
      { value: "before", selected: true },
    ];
    expect(state.currencyPosition).toBe("before");

    state.settings.global.currency[1].value = [
      { value: "after", selected: false },
      { value: "before", selected: false },
    ];
    expect(state.currencyPosition).toBe("after");
  });

  test("Currency symbol", () => {
    state.settings.global.currency[0].value = "₽";
    expect(state.currencySymbol).toBe("₽");
  });

  test("Locale", () => {
    state.settings.global.base[1].value = [
      { value: "en", selected: false },
      { value: "ru", selected: true },
    ];
    expect(state.locale).toBe("ru");

    state.locale = "en";
    expect(state.settings.global.base[1].value).toStrictEqual([
      { value: "en", selected: true },
      { value: "ru", selected: false },
    ]);

    state.settings.global.base[1].value = [
      { value: "en", selected: false },
      { value: "ru", selected: false },
    ];
    expect(state.locale).toBe("en");
  });

  test("Theme", () => {
    state.settings.global.base[0].value = [
      { value: "light", selected: false, },
      { value: "dark", selected: true, },
    ];
    expect(state.theme).toBe("dark");

    state.theme = "light";
    expect(state.settings.global.base[0].value).toStrictEqual([
      { value: "light", selected: true, },
      { value: "dark", selected: false, },
    ]);

    state.settings.global.base[0].value = [
      { value: "light", selected: false, },
      { value: "dark", selected: false, },
    ];
    expect(state.theme).toBe("lightTheme");
  });

});
