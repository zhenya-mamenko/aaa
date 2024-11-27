import "../localStorageMock";
import { mountComponent, appStubs, baseStubs, } from "./utils";
// @ts-ignore
import App from "@/App.vue";


jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
  setLocale: (locale: string) => {},
}));

jest.mock("@/services/ConfigDataService", () => ({
  updateOrCreate: () => Promise.resolve({ data: {}, status: 200, }),
}));

jest.mock("@/services/DataService", () => ({
  getPortfolio: () => Promise.resolve({ data: [], }),
}));


describe("App", () => {

  function mount(data: any) {
    return mountComponent(
      App,
      {
        simpleStubs: ["v-btn", "v-divider", "v-spacer", "form-dialog", "v-data-table", "v-toolbar", ],
        stubs: [...baseStubs, ...appStubs, "PortfolioPage", ],
      },
      {},
      {
        drawer: false,
        page: "portfolio",
        pageProps: {},
        ...data,
      },
    );
  }

  it("Should render", () => {
    const wrapper = mount({});

    expect(wrapper.html()).toMatchSnapshot();
  });

  it("Should contain the menu", () => {
    const wrapper = mount({});

    const menuItems = wrapper.findAll("[data-testid='app-menu'] div.v-list-item");
    expect(menuItems.length).toBe(10);

    const itemTexts = menuItems.map((item) => item.text());
    [
      "portfolio.title", "assets.state", "assets.statements", "dictionaries", "structures.assets",
      "assets.title", "categories.title", "classes.title", "structures.title", "settings.title",
    ].forEach((text, index) => {
      expect(itemTexts[index]).toContain(text);
    });
  });

});
