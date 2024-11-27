<template>
  <v-app full-height :theme="theme || 'light'">
    <v-app-bar color="primary" scroll-behavior="fully-hide">
      <v-app-bar-nav-icon data-testid="app-icon"
        variant="text"
        @click.stop="drawer = !drawer"
      />
      <v-app-bar-title data-testid="app-title">
        {{ t("app_title") }}
      </v-app-bar-title>
      <v-btn data-testid="app-configure"
        icon="mdi-cog"
        @click="showSettings"
      />
    </v-app-bar>
    <v-navigation-drawer
      color="primary"
      data-testid="app-navigation-drawer"
      :temporary="true"
      v-model="drawer"
    >
      <v-list data-testid="app-menu"
        :items="menu"
        @click:select="menuSelected"
      />
    </v-navigation-drawer>
    <v-main>
      <v-container class="h-100">
        <v-row class="h-100">
          <v-col class="h-100 max" cols="12" lg="10" offset-lg="1" xl="8" offset-xl="2" xxl="6" offset-xxl="3">
            <component :is="pageComponent" v-bind="pageProps"/>
          </v-col>
        </v-row>
        <form-dialog
          :opened="dialog.opened" :params="dialog.params" :title="dialog.title"
          @close="closeDialog" @reset="resetSettings" @save="saveSettings"
        />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { nextTick } from "vue";
import { state } from "@/common/state";
import { t, setLocale } from "@/common/locale";
import { deleteParams, findElement, loadParams, removeReactivity, saveParams } from "@/common/utils";
import { defaultSettings } from "@/common/const";

import { type Settings, type AppElement } from "@/types/common";

import ds from "@/services/ConfigDataService";
import { type ConfigEntry } from "@/types/Config";

import AssetsState from "@/components/AssetsState.vue";
import AssetsValues from "@/components/AssetsValues.vue";
import DictionaryPage from "@/components/DictionaryPage.vue";
import PortfolioPage from "@/components/PortfolioPage.vue";
import StructureCategories from "./components/StructureCategories.vue";


export default {
  computed: {
    menu() {
      const menuItem = (element: AppElement) => ({
        title: t(element.title),
        value: element.key,
      });

      return [
        menuItem(findElement("portfolio")),
        menuItem(findElement("assets_state")),
        menuItem(findElement("statements")),
        { type: "divider" },
        {
          title: t("dictionaries"),
          children: [
            menuItem(findElement("structure_categories")),
            { type: "divider" },
            menuItem(findElement("assets")),
            menuItem(findElement("categories")),
            menuItem(findElement("classes")),
            menuItem(findElement("structures")),
          ]
        },
        { type: "divider" },
        menuItem(findElement("settings")),
      ]
    },
    pageComponent() {
      const components: { [key: string]: any } = {
        assets_state: AssetsState,
        assets: DictionaryPage,
        categories: DictionaryPage,
        classes: DictionaryPage,
        statements: AssetsValues,
        structures: DictionaryPage,
        structure_categories: StructureCategories,
        portfolio: PortfolioPage,
      }
      return components[this.page] ?? components["portfolio"];
    },
    t() {
      return t;
    },
    theme() {
      return state.theme;
    },
  },
  data() {
    return {
      dialog: {
        isGlobal: false,
        opened: false,
        params: {} as Settings,
        title: "",
      },
      drawer: false,
      page: "portfolio",
      pageProps: {} as { [key: string]: any },
    }
  },
  methods: {
    closeDialog() {
      this.dialog.opened = false;
      this.dialog.isGlobal = false;
    },
    menuSelected(event: any) {
      this.drawer = false;
      const item = findElement(event.id);
      if (item.type === "page" || item.type === "complex_dictionary") {
        this.pageProps = {};
        this.page = item.key;
      } else if (item.key === "settings") {
        this.dialog.isGlobal = true;
        this.showSettings();
      } else if (item.type === "dictionary") {
        this.page = item.key;
        this.pageProps.pageKey = item.key;
      }
    },
    resetSettings() {
      this.dialog.opened = false;
      const key = this.dialog.isGlobal ? "global" : this.page;
      deleteParams(key);
      state.settings[key] = removeReactivity(defaultSettings[key]);
      if (this.dialog.isGlobal) {
        this.dialog.isGlobal = false;
        this.updateGlobalSettings();
      }
    },
    saveSettings(newValue: any) {
      this.dialog.opened = false;
      const key = this.dialog.isGlobal ? "global" : this.page;
      saveParams(key, newValue);
      state.settings[key] = newValue;
      if (this.dialog.isGlobal) {
        this.dialog.isGlobal = false;
        this.updateGlobalSettings();
      }
    },
    showSettings() {
      const key = this.dialog.isGlobal ? "global" : this.page;
      this.dialog.params = removeReactivity(state.settings[key]);
      if (this.dialog.isGlobal) {
        this.dialog.title = t("settings.title");
      } else {
        this.dialog.title = `${t("settings.title")}<span class="d-none d-md-inline"> : ${t(findElement(this.page).title)}</span>`;
      }
      this.dialog.opened = true;
    },
    async updateGlobalSettings() {
      state.settings["global"] = loadParams("global") || state.settings["global"];
      if (this.$vuetify.locale.current !== state.locale) {
        this.$vuetify.locale.current = state.locale;
      }
      setLocale(state.locale);
      const data: ConfigEntry = {
        config_name: "currency",
        config_value: {
          symbol: state.currencySymbol,
          position: state.currencyPosition,
        },
      }
      if (!!ds && !!data) {
        await ds.updateOrCreate(data);
      }
      await nextTick();
      if (state.refreshCallbacks[this.page]) {
        await state.refreshCallbacks[this.page]();
      }
    },
  },
  mounted() {
    this.updateGlobalSettings();
    setLocale(state.locale);
    document.title = t("app_title");
  },
}
</script>

<style>
  .max {
    max-height: calc(100vh - 75px) !important;
  }
  .v-data-table__th {
    border-top: 1px solid #546E783F !important;
    border-bottom: 2px solid #546E782F !important;
  }
</style>
