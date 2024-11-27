import { mountComponent, cardStubs, simpleStubs } from "./utils";
// @ts-ignore
import DeleteConfirmationDialog from "@/components/DeleteConfirmationDialog.vue";

jest.mock("@/common/locale", () => ({
  t: (key: string) => key,
}));

describe("DeleteConfirmationDialog", () => {

  function mountDialog(props: any, data: any) {
    return mountComponent(
      DeleteConfirmationDialog,
      {
        simpleStubs,
        stubs: [...cardStubs, "v-dialog"],
      },
      {
        opened: true,
        text: "Test",
        ...props,
      },
      {
        confirmationString: "test",
        ...data,
      }
    );
  }

  it("Should render", () => {
    const wrapper = mountDialog({}, {});

    expect(wrapper.html()).toMatchSnapshot();
  });

  it("Should cointain the right texts", () => {
    const wrapper = mountDialog({}, {});

    const title = wrapper.get("[data-testid='delete-confirmation-dialog-title']");
    expect(title.text()).toEqual("confirmations.title");

    const text = wrapper.get("[data-testid='delete-confirmation-dialog-text']");
    expect(text.text()).toEqual("Test");

    const confirmText = wrapper.get("[data-testid='delete-confirmation-dialog-confirm-text']");
    expect(confirmText.text()).toEqual("confirmations.delete_confirm");
  });

  it("Should enable/disable the delete button", () => {
    const wrapper = mountDialog({}, {});

    const input = wrapper.get("[data-testid='delete-confirmation-dialog-input']");
    expect(input.attributes("modelvalue")).toEqual("test");

    const disabled = wrapper.get("[data-testid='delete-confirmation-dialog-delete-button']");
    expect(disabled.attributes("disabled")).toEqual("true");

    const wrapper2 = mountDialog({},
      {
        confirmationString: "delete",
      }
    );

    const input2 = wrapper2.get("[data-testid='delete-confirmation-dialog-input']");
    expect(input2.attributes("modelvalue")).toEqual("delete");

    const enabled = wrapper2.get("[data-testid='delete-confirmation-dialog-delete-button']");
    expect(enabled.attributes("disabled")).toEqual("false");
  });

});
