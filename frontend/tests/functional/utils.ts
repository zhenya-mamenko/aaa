import { mount } from "@vue/test-utils";
import { createVuetify } from 'vuetify';


interface Stub {
  name: string;
  template?: string;
  tag?: string;
}

interface Stubs {
  simpleStubs?: string[];
  stubs?: Array<string | Stub>;
}


export const simpleStubs = [
  "v-autocomplete", "v-btn", "v-divider", "v-select", "v-spacer", "v-switch", "v-text-field",
];

export const appStubs = [
  "v-app",
  { name: "v-app-bar-nav-icon", },
  "v-app-bar-title",
  "v-app-bar",
  "v-content",
  "v-main",
  "v-navigation-drawer",
];

export const baseStubs = [
  "v-btn-toggle",
  "v-dialog",
  {
    name: "v-form",
    template: "<form><slot /></form>",
  },
  "v-icon",
  "v-toolbar",
  "v-toolbar-title",
  "v-responsive",
];

export const cardStubs = [
  "v-card", "v-card-actions", "v-card-title", "v-card-text",
];

export const gridStubs = [
  "v-col", "v-container", "v-row",
];

export const listStubs = [
  "v-list",
  "v-list-item",
  "v-list-subheader",
  "v-list-item-subtitle",
  "v-list-item-title",
  "v-list-item-group",
  "v-list-item-action",
  "v-list-img",
  "v-list-item-media",
];

export const stubs = [
  ...appStubs,
  ...baseStubs,
  ...cardStubs,
  ...gridStubs,
  ...listStubs,
];


export function createStubs(simpleStubs: string[], stubs: Array<string | Stub>) {
  const result: any = {};
  for (const stub of simpleStubs) {
    result[stub] = true;
  }
  for (const stub of stubs) {
    if (typeof stub === "string") {
      result[stub] = {
        template: "<div><slot /></div>",
      };
      continue;
    }
    if (typeof stub === "object") {
      if (!stub.name) continue;
      if (stub.template) {
        const { name, template } = stub;
        result[name] = { template };
      } else if (stub.tag) {
        const { name, tag } = stub;
        result[name] = {
          template: `<${tag}><slot /></${tag}>`,
        };
      } else {
        result[stub.name] = true;
      }
    }
  }
  return result;
}

export function mountComponent(component: any, stubs: string[] | Stubs, props: any, data: any, options: any = {}) {
  const vuetify = createVuetify();
  let s: any;
  if (Array.isArray(stubs)) {
    s = createStubs(stubs, []);
  } else {
    s = createStubs(stubs.simpleStubs || [], stubs.stubs || []);
  }

  return mount(component, {
    global: {
      plugins: [vuetify],
      stubs: s,
    },
    props,
    data: () => data,
    ...options,
  });
}
