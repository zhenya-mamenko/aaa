<template>
  <v-data-table data-testid="portfolio-page-data-table"
    class="h-100"
    :headers="headers"
    hide-default-footer
    :items="portfolio"
    items-per-page="100"
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
    <template v-slot:item="{ item }">
      <tr>
        <td v-for="header in Object.keys(headers)"
          :key="header"
          :align="headers[header as any].align ?? 'start'"
        >
          {{ headers[header as any].key !== "current_percent" ? (headers[header as any] as any).value(item) : ""}}
          <div style="text-wrap-mode: nowrap;" v-if="headers[header as any].key === 'current_percent'">
            {{ item.out_current_percentile }}
            <v-icon
              v-if="Math.abs(item.current_percentile - item.structure_percentile) > parseFloat(params.diffWarning.value)*10"
              color="warning"
              icon="mdi-alert"
              size="x-small"
            />
          </div>
        </td>
      </tr>
    </template>
    <template v-slot:bottom>
      <v-toolbar flat>
          <v-btn-toggle
            class="ms-3 me-3"
            density="comfortable"
            mandatory
            :rounded="4"
            v-model="action"
          >
            <v-btn
              v-for="item in actionItems"
              color="primary-darken-3"
              :data-testid="`portfolio-page-action-${item.value}`"
              :key="item.value"
              :value="item.value"
            >
              <v-icon class="d-inline-block d-md-none pa-0 mt-n1 ms-n1">{{ item.icon }}</v-icon>
              <span class="d-none d-md-inline-block">{{ item.title }}</span>
            </v-btn>
          </v-btn-toggle>
          <v-responsive class="w-25">
            <v-text-field
              class="ms-3 me-3"
              data-testid="portfolio-page-summa-input"
              density="compact"
              hide-details
              hide-spin-buttons
              :prefix="currency.position === 'before' ? currency.symbol : undefined"
              single-line
              :suffix="currency.position === 'after' ? currency.symbol : undefined"
              type="number"
              v-model="summa"
            />
        </v-responsive>
        <v-divider class="ms-1 me-1" vertical />
        <v-btn
          color="primary-darken-3"
          data-testid="portfolio-page-calculate-button"
          :disabled="isNaN(parseFloat(summa)) || parseFloat(summa) < 0 || (parseFloat(summa) === 0 && action === 'replenishment')"
          @click="calculate"
        >
          <v-icon class="d-inline-block d-md-none pa-0 mt-n1 ms-n1" :size="36">mdi-calculator-variant</v-icon>
          <span class="d-none d-md-inline-block ms-1 me-2">{{ t("portfolio.calculate") }}</span>
        </v-btn>
        <v-btn
          color="primary-darken-3"
          data-testid="portfolio-page-reset-button"
          :disabled="!isCalculated"
          @click="isCalculated = false"
        >
          <v-icon class="d-inline-block d-md-none pa-0 mt-n1 ms-n2" :size="36">mdi-close-box</v-icon>
          <span class="d-none d-md-inline-block me-2">{{ t("portfolio.reset") }}</span>
        </v-btn>
      </v-toolbar>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { state } from "@/common/state";
import { t } from "@/common/locale";
import { calculateRebalancing, calculateReplenishment, findElement, loadParams } from "@/common/utils";

import ds from "@/services/DataService";
import { type PortfolioResponse } from "@/types/Types";


const pageKey = "portfolio";

export default defineComponent({
  computed: {
    actionItems() {
      return [
        {
          icon: "mdi-plus-box",
          title: t('portfolio.replenishment'),
          value: 'replenishment', 
        },
        {
          icon: "mdi-chart-pie",
          title: t('portfolio.rebalancing'),
          value: 'rebalancing',
        },
      ]
    },
    currency() {
      return {
        position: state.currencyPosition,
        symbol: state.currencySymbol
    };
    },
    headers() {
      const columns = this.params.columns;
      if (!columns) return [];
      const headers = columns
        .filter(column => column.visible)
        .map(column => {
          const header: any = this.headersRaw.find(header => header.key === column.key);
          header.title = t(column.title);
          header.align = header.align as "start" | "center" | "end";
          return header;
        });
        if (this.isCalculated) {
          headers.push({
            align: "left",
            key: "calculated", 
            maxWidth: "130px",
            noWrap: true,
            title: t("portfolio.result"),
            value: (item: any) => item.calculated,
            width: "80px",
          });
        }
        return headers;
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
      portfolio: [] as PortfolioResponse[],
      action: "replenishment",
      headersRaw: [
        {
          key: "category",
          minWidth: "150px",
          value: (item: any) => item.category_name,
        },
        {
          align: "end",
          key: "amount",
          maxWidth: "120px",
          noWrap: true,
          sortRaw(a: PortfolioResponse, b: PortfolioResponse): number {
            return a.amount - b.amount;
          },
          value: (item: any) => item.out_amount,
          width: "80px",
        },
        {
          align: "end",
          key: "target_percent",
          maxWidth: "120px",
          noWrap: true,
          sortRaw: (a: PortfolioResponse, b: PortfolioResponse): number => {
            return a.structure_percentile - b.structure_percentile;
          },
          value: (item: any) => item.out_structure_percentile,
          width: "90px",
        },
        {
          align: "end",
          key: "current_percent",
          maxWidth: "120px",
          noWrap: true,
          sortRaw: (a: PortfolioResponse, b: PortfolioResponse): number => {
            return a.current_percentile - b.current_percentile;
          },
          value: (item: any) => item.out_current_percentile,
          width: "90px",
        },
      ],
      icon: "",
      isCalculated: false,
      isLoading: true,
      summa: "",
      title: "",
    }
  },
  methods: {
    calculate() {
      const action = this.action;
      const summa = parseFloat(this.summa);
      if (action === "replenishment") {
        calculateReplenishment(this.portfolio, summa);
      } else if (action === "rebalancing") {
        calculateRebalancing(this.portfolio, summa);
      }
      this.portfolio.forEach((item: any) => {
          let s = String(item.calculated);
          if (s.length > 0) {
            s = s.replace(/(\d)(?=(\d{3})+(\D|$))/g, "$1,");
            s = this.currency.position === "before" ? `${this.currency.symbol} ` + s : s + ` ${this.currency.symbol}`;
          }
          item.calculated = s;
        });
      this.isCalculated = true;
    },
    async loadData() {
      this.isLoading = true;
      this.title = t(findElement(pageKey).title);
      this.icon = findElement(pageKey).icon;
      if (ds) {
        const portfolio = await ds.getPortfolio();
        this.portfolio = portfolio;
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
