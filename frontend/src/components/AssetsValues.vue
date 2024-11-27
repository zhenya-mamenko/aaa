<template>
  <v-data-table data-testid="assets-values-data-table"
    class="h-100"
    :headers="headers"
    :filter-keys="['asset', 'category', 'class', 'date', ]"
    :items="statements"
    :loading="isLoading"
    :loading-text="t('messages.loading')"
    :search="search"
    sort-asc-icon="mdi-triangle-small-up"
    sort-desc-icon="mdi-triangle-small-down"
    :sticky="true"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-icon
          class="ms-3 me-3"
          size="large"
        >
          {{ icon }}
        </v-icon>
        <v-toolbar-title
          class="d-none d-md-block ms-0"
        >
          {{ title }}
        </v-toolbar-title>
        <v-responsive class="w-25">
          <v-text-field data-testid="assets-values-search-input"
            clearable
            clear-icon="mdi-close"
            density="compact"
            hide-details
            :label="t('search')"
            persistent-clear
            prepend-inner-icon="mdi-magnify"
            single-line
            v-model="search"
          />
        </v-responsive>
        <v-divider class="ms-3 me-3" vertical />
        <v-btn data-testid="assets-values-add-button"
          class="me-2"
          color="primary-darken-3"
          @click="createItem"
        >
          {{ t("buttons.add") }}
        </v-btn>
    </v-toolbar>
  </template>
  </v-data-table>
  <form-dialog
    :opened="dialog.opened"
    :params="dialog.params"
    :show-reset-button="false"
    :title="dialog.title"
    @close="dialog.opened = false;"
    @save="save"
  />
  <v-snackbar
    :timeout="info.timeout || 2000"
    :color="info.color || 'success'"
    vertical
    v-model="info.show"
  >
    {{ info.text }}
  </v-snackbar>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { state } from "@/common/state";
import { t } from "@/common/locale";
import { findElement, loadParams, parseAxiosError } from "@/common/utils";

import ds from "@/services/AssetsDataService";
import { type Asset, type AssetValue, type AssetsValuesResponse } from "@/types/Assets";


const pageKey = "statements";

export default defineComponent({
  computed: {
    headers() {
      const columns = this.params.columns;
      if (!columns) return [];
      return columns
        .filter(column => column.visible)
        .map(column => {
          const header: any = this.headersRaw.find(header => header.key === column.key);
          header.title = t(column.title);
          header.align = header.align as "start" | "center" | "end";
          return header;
        });
    },
    params() {
      return state.settings[pageKey];
    },
    t() {
      return t;
    },
  },
  data() {
    return {
      statements: [] as AssetsValuesResponse[],
      dialog: {
        opened: false,
        params: {},
        title: "",
      },
      headersRaw: [
        {
          key: "class",
          value: (item: any) => item.class_name,
        },
        {
          key: "category",
          value: (item: any) => item.category_name,
        },
        {
          key: "asset",
          minWidth: "200px",
          value: (item: any) => `${item.asset_name}${item.asset_ticker !== "" ? ` (${item.asset_ticker})` : ""}`,
        },
        {
          key: "date",
          maxWidth: "90px",
          noWrap: true,
          sortRaw(a: AssetsValuesResponse, b: AssetsValuesResponse): number {
            return a.asset_value_datetime > b.asset_value_datetime ? 1 :
              (a.asset_value_datetime < b.asset_value_datetime ? -1 : 0);
          },
          value: (item: any) => (new Date(item.asset_value_datetime)).toLocaleDateString(state.locale),
          width: "90px",
        },
        {
          align: "end",
          key: "amount",
          maxWidth: "130px",
          noWrap: true,
          sortRaw(a: AssetsValuesResponse, b: AssetsValuesResponse): number {
            return a.amount - b.amount;
          },
          value: (item: any) => item.out_amount,
          width: "90px",
        },
      ],
      icon: "",
      info: {
        color: "success",
        show: false,
        text: "",
        timeout: 2000,
      } as Partial<{ color: string, show: boolean, text: string, timeout: number }>,
      isLoading: true,
      title: "",
      search: "",
    }
  },
  methods: {
    async add(item: AssetValue) {
      try {
        await ds.createValue(item);
        this.loadData();
        this.dialog.opened = false;
        this.info = {
          show: true,
          text: t("messages.added"),
        }
      } catch (error: any) {
        const res = parseAxiosError(error);
        this.info = {
          color: "error",
          show: true,
          timeout: 3000,
          text: Array.isArray(res) ? t(res[0], ...res.slice(1)) : t(res),
        }
        console.error(error);
      }
    },
    async createItem() {
      this.dialog.title = t("buttons.add") + " " + t("assets.statements.2").toLowerCase();
      this.dialog.params = {
        asset_id: {
          rules: [
            "required",
          ],
          title: t("assets.1"),
          type: "autocomplete",
          value: (await ds.getAll())
            .sort((a, b) => a.asset_name.toLowerCase() > b.asset_name.toLowerCase() ? 1 : -1)
            .map((a: Asset) => ({
              value: a.asset_id,
              title: a.asset_name,
              selected: false,
            })),
        },
        amount: {
          cols: 3,
          rules: [
            "required",
            "number",
            ["min_value", 0.1, ],
          ],
          title: t("assets.amount") + ", " + state.currencySymbol,
          type: "number",
          value: "",
        },
      };
      this.dialog.opened = true;
    },
    async loadData() {
      this.isLoading = true;
      this.title = t(findElement(pageKey).title);
      this.icon = findElement(pageKey).icon;
      if (ds) {
        const statements = await ds.getValues();
        this.statements = statements;
      }
      this.isLoading = false;
    },
    save(data: any) {
      const result = {} as any;
      Object.entries(data).forEach(([key, value]) => {
        if (Array.isArray((value as any).value)) {
          result[key] = (value as any).value.find((item: any) => item.selected).value ?? null;
        } else {
          result[key] = (value as any).value;
        }
      });
      result.amount = Math.round(result.amount * 100);
      this.add(result);
    },

  },
  mounted() {
    state.settings[pageKey] = loadParams(pageKey) || state.settings[pageKey];
    state.refreshCallbacks[pageKey] = this.loadData;
    this.loadData();
  },
});
</script>
