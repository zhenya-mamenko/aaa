import { mount } from "@vue/test-utils";
import { createVuetify } from 'vuetify';
// @ts-ignore
import FormItem from "@/components/FormItem.vue";

jest.mock("@/common/locale", () => ({
    t: (key: string) => key,
}));

describe("FormItem", () => {
  let vuetify: any;

  beforeEach(() => {
    vuetify = createVuetify();
  });

  it("Should render text-field", () => {
    const wrapper = mount(FormItem, {
      global: {
        plugins: [vuetify],
        stubs: {
          "v-text-field": true,
        },
      },
      propsData: {
        params: {
          value: "$",
          title: "Currency",
        },
      },
    });

    const cmp = wrapper.get("[data-testid='text-field-currency']");
    expect(cmp.attributes("type")).toEqual("text");
    expect(cmp.attributes("modelvalue")).toEqual("$");
    expect(cmp.attributes("label")).toEqual("Currency");

    const wrapper2 = mount(FormItem, {
      global: {
        plugins: [vuetify],
        stubs: {
          "v-text-field": true,
        },
      },
      propsData: {
        params: {
          value: 100,
          title: "Amount",
        },
      },
    });

    const cmp2 = wrapper2.get("[data-testid='text-field-amount']");
    expect(cmp2.attributes("type")).toEqual("number");
    expect(cmp2.attributes("modelvalue")).toEqual("100");
    expect(cmp2.attributes("label")).toEqual("Amount");
  });

  it("Should render select", () => {
    const wrapper = mount(FormItem, {
      global: {
        plugins: [vuetify],
        stubs: {
          "v-select": true,
        },
      },
      propsData: {
        params: {
          value: [
            { value: "before", title: "Before", },
            { value: "after", title: "After", selected: true, },
          ],
          title: "settings.position",
        },
      },
    });

    const cmp = wrapper.get("[data-testid='select-settings-position']");
    expect(cmp.attributes("modelvalue")).toEqual("after");
    expect(cmp.attributes("label")).toEqual("settings.position");
  });

  it("Should render autocomplete", () => {
    const wrapper = mount(FormItem, {
      global: {
        plugins: [vuetify],
        stubs: {
          "v-autocomplete": true,
        },
      },
      propsData: {
        params: {
          value: [
            { value: "before", title: "Before", },
            { value: "after", title: "After", selected: true, },
          ],
          title: "settings.position",
          type: "autocomplete",
        },
      },
    });

    const cmp = wrapper.get("[data-testid='autocomplete-settings-position']");
    expect(cmp.attributes("modelvalue")).toEqual("after");
    expect(cmp.attributes("label")).toEqual("settings.position");
  });

  it("Should render switch", () => {
    const wrapper = mount(FormItem, {
      global: {
        plugins: [vuetify],
        stubs: {
          "v-switch": true,
        },
      },
      propsData: {
        params: {
          value: true,
          title: "Show",
        },
      },
    });
    const cmp = wrapper.get("[data-testid='switch-show']");
    expect(cmp.attributes("modelvalue")).toEqual("true");
    expect(cmp.attributes("label")).toEqual("Show");
  });

});
