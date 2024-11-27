import { nextTick } from "vue";
import { mountComponent, baseStubs } from "./utils";
import db from "../db_data.json"
// @ts-ignore
import AssetsValues from "@/components/AssetsValues.vue";


const statements = db.assets_values;

jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

jest.mock("@/services/AssetsDataService", () => ({
  getValues: () => Promise.resolve({ data: statements, }),
}));


describe("AssetsValues", () => {

  function mount(data: any) {
    return mountComponent(
      AssetsValues,
      {
        simpleStubs: ["v-btn", "v-divider", "v-spacer", "form-dialog", ],
        stubs: [...baseStubs, "v-pagination", ],
      },
      {},
      {
        icon: "mdi-invoice-text-clock",
        statements,
        title: "Test Statements",
        search: "",
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

    expect(wrapper.text()).toContain("Test Statements");
    const headers = wrapper.findAll("th");
    expect(headers.length).toBe(3);
    expect(headers[0].text()).toBe("date.title");
    expect(headers[1].text()).toBe("assets.1");
    expect(headers[2].text()).toBe("assets.amount");
  });

  it("Should contain the right data", () => {
    const wrapper = mount({});

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(3);

    const data = rows[0].findAll("td");
    expect(data.length).toBe(3);
    expect(data[0].text()).toBe("1/1/2023");
    expect(data[1].text()).toBe("Asset 1 (A1)");
    expect(data[2].text()).toBe("100");
  });

  it("Should filter the data", async () => {
    const wrapper = mount({});

    (wrapper.vm as AssetsValues).search = "Asset 2";
    await nextTick();

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(2);
    expect(rows[0].text()).toContain("Asset 2");
    expect(rows[1].text()).toContain("Asset 23");
  });

});
