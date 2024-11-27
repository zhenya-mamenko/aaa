import { nextTick } from "vue";
import { mountComponent, baseStubs } from "./utils";
import db from "../db_data.json"
// @ts-ignore
import PortfolioPage from "@/components/PortfolioPage.vue";


const portfolio = db.portfolio;

jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

jest.mock("@/services/DataService", () => ({
  getPortfolio: () => Promise.resolve({ data: portfolio, }),
}));


describe("PortfolioPage", () => {

  function mount(data: any) {
    return mountComponent(
      PortfolioPage,
      {
        simpleStubs: ["v-btn", "v-divider", "v-spacer", ],
        stubs: [...baseStubs, ],
      },
      {},
      {
        action: "replenishment",
        icon: "mdi-briefcase-variant",
        isCalculated: false,
        portfolio,
        summa: "0",
        title: "Test Portfolio",
        ...data,
      },
    );
  }

  it("Should render", () => {
    const wrapper = mount({});

    expect(wrapper.html()).toMatchSnapshot();
  });

  it("Should contain the right text", () => {
    const wrapper = mount({});

    expect(wrapper.text()).toContain("Test Portfolio");
    const headers = wrapper.findAll("th");
    expect(headers.length).toBe(4);
    expect(headers[0].text()).toBe("categories.1");
    expect(headers[1].text()).toBe("portfolio.target_percent");
    expect(headers[2].text()).toBe("portfolio.current_percent");
    expect(headers[3].text()).toBe("assets.amount");
  });

  it("Should contain the right data", () => {
    const wrapper = mount({});

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(3);

    const data = rows[0].findAll("td");
    expect(data.length).toBe(4);
    expect(data[0].text()).toBe("Category 1");
    expect(data[1].text()).toBe("10%");
    expect(data[2].text()).toBe("20%");
    expect(data[3].text()).toBe("$100.00");
  });

  it("Should do calculations and reset", async () => {
    const wrapper = mount({});
    const input = wrapper.get("[data-testid='portfolio-page-summa-input'] input");
    const button = wrapper.get("[data-testid='portfolio-page-calculate-button']");
    const vm = (wrapper.vm as PortfolioPage);

    expect(input.attributes("value")).toBe("0");
    expect(button.attributes("disabled")).toBe("true");

    vm.action = "rebalancing";
    await nextTick();
    expect(button.attributes("disabled")).toBe("false");

    vm.calculate();
    await nextTick();
    const headers = wrapper.findAll("th");
    expect(headers.length).toBe(5);
    expect(headers[4].text()).toBe("portfolio.result");

    vm.isCalculated = false;
    await nextTick();
    expect(wrapper.findAll("th").length).toBe(4);
  });

});
