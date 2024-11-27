// @ts-ignore
import { setLocale, t } from "@/common/locale";
// @ts-ignore
import { state } from "@/common/state";


jest.mock("@/common/state", () => ({
  state: {
    locale: "en",
    messages: {
      "app_title": "Assets Allocation",
      "actions": "Actions",
      "assets.amount": "Amount",
      "assets.title": "Assets",
    },
  },
}));

jest.mock("@/messages.json", () => (
  {
    en: {
      app_title: "Assets Allocation {0}",
      actions: "Actions",
      assets: {
        amount: "Amount",
        title: "Assets",
      },
    },
    ru: {
      app_title: "Распределение активов",
      actions: "Действия",
      assets: {
        amount: "Сумма",
        title: "Активы",
      },
    },
  }
));


describe("Locale functions", () => {

  test("Set locale", () => {
    setLocale("ru");

    expect(state.locale).toBe("ru");
    expect(state.messages).toStrictEqual({
      app_title: "Распределение активов",
      actions: "Действия",
      "assets.amount": "Сумма",
      "assets.title": "Активы",
    });
  });

  test("Translate", () => {
    setLocale("en");

    expect(t("assets.amount")).toBe("Amount");
    expect(t("assets.title")).toBe("Assets");
    expect(t("assets.unknown_info_or_something")).toBe("unknown info or something");

    expect(t("app_title", "assets.amount")).toBe("Assets Allocation Amount");
  });

});
