import { reactive } from "vue";

import { type Messages, type State, type SettingsMap } from "@/types/common";
import { removeReactivity } from "@/common/utils";
import { defaultSettings } from "@/common/const";


export const state: State = reactive({
  get currencyPosition(): string {
    return this.settings.global.currency[1].value.find((item: any) => item.selected)?.value || "after";
  },
  get currencySymbol(): string {
    return this.settings.global.currency[0].value;
  },


  get locale(): string {
    return this.settings.global.base[1].value.find((item: any) => item.selected)?.value || "en";
  },
  set locale(value: string) {
    const langs = this.settings.global.base[1].value;
    this.settings.global.base[1].value = langs.map((item: any) => ({ ...item, selected: item.value === value }));
  },

  messages: {} as Messages,
  settings: removeReactivity(defaultSettings) as SettingsMap,

  get theme(): string {
    return this.settings.global.base[0].value.find((item: any) => item.selected)?.value || "lightTheme";
  },
  set theme(value: string) {
    const langs = this.settings.global.base[0].value;
    this.settings.global.base[0].value = langs.map((item: any) => ({ ...item, selected: item.value === value }));
  },

  refreshCallbacks: {} as { [key: string]: Function },
});
