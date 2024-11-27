import { createStubs, mountComponent } from '../functional/utils';

describe('Functional utils', () => {

  test('createStubs', () => {
    const stubs = createStubs(['a', 'b'], [
      'c',
      { name: 'd', template: '<div></div>' },
      { name: 'e', tag: 'span' },
      { name: 'f' },
    ]);
    expect(stubs).toStrictEqual({
      a: true,
      b: true,
      c: { template: '<div><slot /></div>' },
      d: { template: '<div></div>' },
      e: { template: '<span><slot /></span>' },
      f: true,
    });
  });


  test('mountComponent', () => {
    const component = {
      template: `
        <v-card>
          <v-card-title>
            Test
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="b" />
          </v-card-text>
          <v-card-actions>
            <v-btn :text="a"></v-btn>
          </v-card-actions>
        </v-card>
      `,
      props: {
        a: String,
      },
    };
    const stubs = {
      simpleStubs: [ "v-btn", "v-text-field" ],
      stubs: [ "v-card", "v-card-title", "v-card-text", "v-card-actions", ]
    };
    const props = { a: "Test" };
    const data = { b: 1 };
    const wrapper = mountComponent(component, stubs, props, data);
    expect(wrapper.html()).toMatchInlineSnapshot(`
      "<div>
        <div> Test </div>
        <div>
          <v-text-field-stub modelvalue="1"></v-text-field-stub>
        </div>
        <div>
          <v-btn-stub text="Test"></v-btn-stub>
        </div>
      </div>"
    `);
  });

});
