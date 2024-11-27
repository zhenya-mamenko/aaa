import { mountComponent, baseStubs } from "./utils";
import db from "../db_data.json"
// @ts-ignore
import AssetsState from "@/components/AssetsState.vue";


const assets_state = db.assets_state;

jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

jest.mock("@/services/AssetsDataService", () => ({
  getState: () => Promise.resolve({ data: assets_state, }),
}));


describe("AssetsState", () => {

  function mount(data: any) {
    return mountComponent(
      AssetsState,
      {
        simpleStubs: ["v-btn", "v-divider", "v-spacer", ],
        stubs: [...baseStubs, "v-pagination", ],
      },
      {},
      {
        icon: "mdi-finance",
        assets: assets_state,
        title: "Test Assets State",
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

    expect(wrapper.text()).toContain("Test Assets State");
    const headers = wrapper.findAll("tr:first-child th");
    expect(headers.length).toBe(3);
    expect(headers[0].text()).toBe("assets.1");
    expect(headers[1].text()).toBe("assets.amount");
    expect(headers[2].text()).toBe("assets.prev_change");
  });

  it("Should contain the right data", () => {
    const wrapper = mount({});

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(5);

    const data = rows[0].findAll("td");
    expect(data.length).toBe(3);
    expect(data[0].text()).toBe("Asset 1 (A1)");
    expect(data[1].text()).toBe("$ 100");
    expect(data[2].text()).toBe("25%");
    expect(data[2].html()).toContain("mdi-triangle-small-up");

    expect(rows[1].findAll("td")[2].html()).toContain("mdi-triangle-small-down");
  });

});
