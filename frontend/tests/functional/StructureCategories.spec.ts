import { mountComponent, baseStubs } from "./utils";
import db from "../db_data.json"
// @ts-ignore
import StructureCategories from "@/components/StructureCategories.vue";


const structures = db.structures;
const categories = db.categories;

jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

jest.mock("@/services/StructuresDataService", () => ({
  getAll: (structure_id?: number) => Promise.resolve({ data: structure_id === undefined ? structures : categories, }),
}));


describe("StructureCategories", () => {

  function mount(data: any) {
    return mountComponent(
      StructureCategories,
      {
        simpleStubs: ["v-btn", "v-divider", "v-spacer", "form-dialog", "delete-confirmation-dialog"],
        stubs: [...baseStubs, ],
      },
      {},
      {
        categories,
        icon: "mdi-label-percent",
        is_current: false,
        structures,
        structure_id: 0,
        title: "Test StructureCategories",
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

    expect(wrapper.text()).toContain("Test StructureCategories");
    const headers = wrapper.findAll("th");
    expect(headers.length).toBe(3);
    expect(headers[0].text()).toBe("categories.1");
    expect(headers[1].text()).toBe("portfolio.target_percent");
    expect(headers[2].text()).toBe("actions");
  });

  it("Should contain the right data", () => {
    const wrapper = mount({});

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(4);

    const data = rows[0].findAll("td");
    expect(data.length).toBe(3);
    expect(data[0].text()).toBe("Category 1");
    expect(data[1].text()).toBe("10%");
    expect(data[2].text()).toContain("mdi-pencil");
    expect(data[2].text()).toContain("mdi-delete");
  });

});
