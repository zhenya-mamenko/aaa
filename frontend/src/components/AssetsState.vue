<template>
  <v-data-table data-testid="assets-state-data-table"
    class="h-100"
    :headers="headers"
    :items="assets"
    :loading="isLoading"
    :loading-text="t('messages.loading')"
    sort-asc-icon="mdi-triangle-small-up"
    sort-desc-icon="mdi-triangle-small-down"
    :sticky="true"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-icon
          class="ms-3"
          size="large"
        >
          {{ icon }}
        </v-icon>
        <v-toolbar-title>{{ title }}</v-toolbar-title>
      </v-toolbar>
    </template>
    <template v-slot:item.prev_change="{ value }">
      <div style="text-wrap-mode: nowrap;">
        <span class="me-n1">{{ value.value }}</span>
        <v-icon color="error" v-if="value.sign === -1" icon="mdi-triangle-small-down"></v-icon>
        <v-icon color="success" v-if="value.sign === 1" icon="mdi-triangle-small-up"></v-icon>
      </div>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { state } from "@/common/state";
import { t } from "@/common/locale";
import { findElement, loadParams } from "@/common/utils";

import ds from "@/services/AssetsDataService";
import { type AssetsStateResponse } from "@/types/Assets";

const pageKey = "assets_state";

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
      assets: [] as AssetsStateResponse[],
      headersRaw: [
        {
          key: "asset",
          minWidth: "200px",
          value: (item: any) => `${item.asset_name}${item.asset_ticker !== "" ? ` (${item.asset_ticker})` : ""}`,
        },
        {
          align: "end",
          key: "amount",
          maxWidth: "130px",
          noWrap: true,
          sortRaw(a: AssetsStateResponse, b: AssetsStateResponse): number {
            return a.last - b.last;
          },
          value: (item: any) => item.out_last,
          width: "90px",
        },
        {
          key: "category",
          value: (item: any) => item.category_name,
        },
        {
          key: "class",
          value: (item: any) => item.class_name,
        },
        {
          align: "end",
          key: "prev_amount",
          maxWidth: "130px",
          noWrap: true,
          sortRaw: (a: AssetsStateResponse, b: AssetsStateResponse): number => {
            return !!(state.settings[pageKey].showFromFirst.value) ? a.first - b.first : a.lag - b.lag;
          },
          value: (item: AssetsStateResponse) => !!(state.settings[pageKey].showFromFirst.value) ? item.out_first : item.out_lag,
          width: "90px",
        },
        {
          align: "end",
          key: "prev_change",
          maxWidth: "120px",
          noWrap: true,
          sortRaw: (a: AssetsStateResponse, b: AssetsStateResponse): number => {
            return !!(state.settings[pageKey].showFromFirst.value) ? a.last_first_percent - b.last_first_percent :
              a.last_lag_percent - b.last_lag_percent;
          },
          value: (item: any) => ({
            value: !!(state.settings[pageKey].showFromFirst.value) ? item.out_last_first_percent : item.out_last_lag_percent,
            sign: ((!!(state.settings[pageKey].showFromFirst.value) ? item.last_first_percent : item.last_lag_percent) > 0 ? 1 : (
              (!!(state.settings[pageKey].showFromFirst.value) ? item.last_first_percent : item.last_lag_percent) < 0 ? -1 : 0
            )),
          }),
          width: "90px",
        },
      ],
      icon: "",
      isLoading: true,
      title: "",
    }
  },
  methods: {
    async loadData() {
      this.isLoading = true;
      this.title = t(findElement(pageKey).title);
      this.icon = findElement(pageKey).icon;
      if (ds) {
        const assetsState = await ds.getState();
        this.assets = assetsState;
      }
      this.isLoading = false;
    }
  },
  mounted() {
    state.settings[pageKey] = loadParams(pageKey) || state.settings[pageKey];
    state.refreshCallbacks[pageKey] = this.loadData;
    this.loadData();
  },
});
</script>
