import { mountComponent, simpleStubs, cardStubs, baseStubs } from "./utils";
// @ts-ignore
import FormItem from "@/components/FormItem.vue";
import draggable from "vuedraggable";
// @ts-ignore
import FormDialog from "@/components/FormDialog.vue";


jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

describe("FormDialog", () => {

  function mountDialog(props: any, data: any) {
    const p = {
      prop1: { value: true, title: "prop1", },
      prop2: { value: "test", title: "prop2", },
    };
    const params = {
      columns: [
        { "key": "column1", "visible": true, disabled: true, title: "column1", },
        { "key": "column2", "visible": false, disabled: false, title: "column2", },
      ],
      ...p
    };
    return mountComponent(
      FormDialog,
      {
        simpleStubs: [...simpleStubs, ],
        stubs: [...cardStubs, ...baseStubs, ],
      },
      {
        opened: true,
        title: "Test",
        params,
        ...props,
      },
      {
        columns: params.columns,
        results: p,
        ...data,
      },
      {
        components: {
          draggable,
          FormItem,
        }
      }
    );
  }

  it("Should render", () => {
    const wrapper = mountDialog({}, {});

    expect(wrapper.html()).toMatchSnapshot();
  });

  it("Should cointain the right elements", () => {
    const wrapper = mountDialog({}, {});

    const input = wrapper.get("[data-testid='text-field-prop2']");
    expect(input.attributes("label")).toEqual("prop2");
    expect(input.attributes("modelvalue")).toEqual("test");

    const sw = wrapper.get("[data-testid='switch-prop1']");
    expect(sw.attributes("label")).toEqual("prop1");
    expect(sw.attributes("modelvalue")).toEqual("true");

    expect(wrapper.text()).toContain("settings.columns");

    const columns = wrapper.findAll("[data-testid^='switch-column']");
    expect(columns).toHaveLength(2);
    expect(columns[0].attributes("disabled")).toEqual("true");
    expect(columns[0].attributes("modelvalue")).toEqual("true");
    expect(columns[0].attributes("label")).toEqual("column1");
    expect(columns[1].attributes("disabled")).toEqual("false");
    expect(columns[1].attributes("modelvalue")).toEqual("false");
    expect(columns[1].attributes("label")).toEqual("column2");
  });

  it("Should show/hide the reset button", () => {
    const wrapper = mountDialog({}, {});

    const button = wrapper.get("[data-testid='form-dialog-reset-button']");
    expect(button.isVisible()).toEqual(true);

    const wrapper2 = mountDialog({ showResetButton: false }, {});
    expect(wrapper2.findAll("[data-testid='form-dialog-reset-button']")).toHaveLength(0);
  });

  it("Should emit the right data on save", () => {
    const wrapper = mountDialog({}, {});

    const button = wrapper.get("[data-testid='form-dialog-save-button']");
    button.trigger("click");

    const save = wrapper.emitted("save");
    expect(save).not.toBeUndefined();
    expect((save as any)[0]).toStrictEqual([{
        prop1: { value: true, title: "prop1", },
        prop2: { value: "test", title: "prop2", },
        columns: [
          { "key": "column1", "visible": true, disabled: true, title: "column1", },
          { "key": "column2", "visible": false, disabled: false, title: "column2", },
        ],
      }]);
  });

});
