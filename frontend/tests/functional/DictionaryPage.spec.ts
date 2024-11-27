import { nextTick } from "vue";
import { mountComponent, baseStubs } from "./utils";
import db from "../db_data.json"
// @ts-ignore
import DictionaryPage from "@/components/DictionaryPage.vue";


const classes = db.classes;

jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

jest.mock("@/services/ClassesDataService", () => ({
  getAll: () => Promise.resolve({ data: classes, }),
}));

jest.mock("@/services/AssetsDataService", () => ({
  getAll: () => Promise.resolve({ data: [], }),
}));

jest.mock("@/services/CategoriesDataService", () => ({
  getAll: () => Promise.resolve({ data: [], }),
}));


describe("DictionaryPage", () => {

  function mount(props: any, data: any) {
    return mountComponent(
      DictionaryPage,
      {
        simpleStubs: ["v-btn", "v-divider", "v-spacer", "form-dialog", "delete-confirmation-dialog", ],
        stubs: [...baseStubs, "v-pagination", ],
      },
      {
        pageKey: "classes",
        ...props,
      },
      {
        icon: "mdi-shape-plus",
        items: classes,
        title: "Test",
        search: "",
        ...data,
      },
    );
  }

  it("Should render", () => {
    const wrapper = mount({}, {});

    expect(wrapper.html()).toMatchSnapshot();
  });

  it("Should contain the right text", () => {
    const wrapper = mount({}, {});

    expect(wrapper.text()).toContain("dictionaries: Test");
    const headers = wrapper.findAll("th");
    expect(headers.length).toBe(3);
    expect(headers[0].text()).toBe("id");
    expect(headers[1].text()).toBe("classes.1");
    expect(headers[2].text()).toBe("actions");
  });

  it("Should contain the right data", () => {
    const wrapper = mount({}, {});

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(4);

    const data = rows[0].findAll("td");
    expect(data.length).toBe(3);
    expect(data[0].text()).toBe("1");
    expect(data[1].text()).toBe("Test");
    expect(data[2].text()).toContain("mdi-pencil");
    expect(data[2].text()).toContain("mdi-delete");
  });

  it("Should filter the data", async () => {
    const wrapper = mount({}, {});

    const input = wrapper.get("[data-testid='dictionary-page-search-input'] input");
    input.setValue("Test3");
    await nextTick();

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(2);
    expect(rows[0].text()).toContain("Test3");
    expect(rows[1].text()).toContain("Test33");
  });

});
