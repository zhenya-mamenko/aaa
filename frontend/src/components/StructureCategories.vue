<template>
  <v-data-table data-testid="structure-categories-data-table"
    class="h-100"
    :headers="headers"
    hide-default-footer
    :items="categories"
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
          <v-select
            class="me-2"
            data-testid="structure-categories-structure-select"
            density="compact"
            hide-details
            :items="structures"
            :prepend-inner-icon="structureIcon"
            ref="structureSelect"
            v-model="structure_id"
            @update:modelValue="loadCategories"
          />
        </v-responsive>
        <v-divider class="ms-3 me-3" vertical />
        <v-btn
          class="me-2"
          data-testid="structure-categories-add-button"
          color="primary-darken-3"
          :disabled="structures.length === 0"
          @click="createItem"
        >
          {{ t("buttons.add") }}
        </v-btn>
    </v-toolbar>
  </template>
  <template v-slot:item.actions="{ item }">
      <v-icon class="me-2" size="small" @click="editItem(item)">
        mdi-pencil
      </v-icon>
      <v-icon size="small" @click="confirmDelete(item)">
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:bottom>
      <v-toolbar flat>
        <v-btn
          class="ms-3"
          data-testid="structure-categories-set-as-current-button"
          color="primary-darken-3"
          :disabled="is_current || structureSum !== 100"
          @click="setAsDefault"
        >
          {{ t("structures.set_as_current") }}
        </v-btn>
        <v-divider class="ms-3 me-3" vertical />
        <v-spacer/>
        <v-responsive class="text-right text-h6 me-3">
          {{ structureSum }}%
          <v-icon
            v-if="structureSum !== 100"
            class="ms-1"
            color="error"
            icon="mdi-alert"
            size="small"
          />
        </v-responsive>
      </v-toolbar>
    </template>
  </v-data-table>
  <form-dialog
    :is-saving="isSaving"
    :opened="dialog.opened"
    :params="dialog.params"
    :show-reset-button="false"
    :title="dialog.title"
    @close="close"
    @save="save"
  />
  <delete-confirmation-dialog
    :opened="confirmationDialog.opened"
    :text="confirmationDialog.text"
    @close="confirmationDialog.opened = false"
    @delete="deleteItem(confirmationDialog.id)"
  />
  <v-snackbar data-testid="structure-categories-snackbar"
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

import ds from "@/services/StructuresDataService";
import dsCategories from "@/services/CategoriesDataService";
import { type StructureCategory, type StructureCategoryResponse, type StructureResponse } from "@/types/Structures";
import { type Category } from "@/types/Categories";


const pageKey = "structure_categories";

export default defineComponent({
  computed: {
    headers() {
      const columns = this.params.columns;
      if (!columns) return [];
      const result = columns
        .filter(column => column.visible)
        .map(column => {
          const header: any = this.headersRaw.find(header => header.key === column.key);
          header.title = t(column.title);
          header.align = header.align as "start" | "center" | "end";
          return header;
        });
      result.push({ title: t("actions"), sortable: false, align: "center", maxWidth: "80px", width: "80px", value: "actions", });
      return result;
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
      structures: [] as any[],
      structure_id: "" as string | number,
      categories: [] as StructureCategoryResponse[],
      confirmationDialog: {
        id: 0 as number,
        opened: false,
        text: "",
      },
      dialog: {
        id: 0 as number,
        item: {} as any,
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
          align: "end",
          key: "target_percent",
          maxWidth: "130px",
          noWrap: true,
          sortRaw(a: StructureCategoryResponse, b: StructureCategoryResponse): number {
            return a.percentile > b.percentile ? 1 : (a.percentile < b.percentile ? -1 : 0);
          },
          value: (item: any) => item.out_percentile,
          width: "100px",
        },
      ],
      icon: "",
      info: {
        color: "success",
        show: false,
        text: "",
        timeout: 2000,
      } as Partial<{ color: string, show: boolean, text: string, timeout: number }>,
      is_current: false,
      isLoading: false,
      isSaving: false,
      structureIcon: "mdi-list-box",
      structureSum: 0,
      title: "",
    }
  },
  methods: {
    async add(item: StructureCategory) {
      try {
        await ds.create(item);
        this.loadCategories();
        this.close();
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
    close() {
      this.dialog.opened = false;
      this.dialog.item = {};
      this.dialog.id = 0;
    },
    async createItem() {
      this.dialog.title = t("buttons.add") + " " + t("structures.element").toLowerCase();
      this.dialog.params = await this.makeParams();
      this.dialog.opened = true;
    },
    async confirmDelete(item: StructureCategoryResponse) {
      this.confirmationDialog.text = t(
        "confirmations.delete_text", item.category_name
      );
      this.confirmationDialog.id = item.category_id;
      this.confirmationDialog.opened = true;
    },
    async deleteItem(id: number) {
      try {
        this.confirmationDialog.opened = false;
        await ds.delete(this.structure_id as number, id);
        this.loadCategories()
        this.info = {
          show: true,
          text: t("messages.deleted"),
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
    async editItem(item: StructureCategory) {
      this.dialog.item = item;
      this.dialog.id = item.category_id;
      this.dialog.params = await this.makeParams();
      this.dialog.title = t("buttons.edit") + " " + t("structures.element").toLowerCase();
      this.dialog.opened = true;
    },
    async loadData() {
      this.isLoading = true;
      this.title = t(findElement(pageKey).title);
      this.icon = findElement(pageKey).icon;
      if (!ds) return;
      const structures = await ds.getAll() as StructureResponse[];
      this.structures = structures.map((item: StructureResponse) => ({
        value: item.structure_id,
        title: `${item.structure_name}${item.is_current ? ` ✔` : ""}`,
        is_current: item.is_current,
      }));
      if (this.structures.length !== 0) {
        this.structure_id = structures.find((item: any) => Boolean(item.is_current))?.structure_id || structures[0].structure_id;
        await this.loadCategories();
      }
      this.isLoading = false;
    },
    async loadCategories() {
      if (!ds || !this.structure_id) return;
      this.isLoading = true;
      (this.$refs.structureSelect as HTMLInputElement)?.blur();
      this.is_current = this.structures.find((item: any) => item.value === this.structure_id)?.is_current;
      const categories = await ds.getAll(this.structure_id as number) as StructureCategoryResponse[];
      this.categories = categories;
      this.structureSum = categories.reduce((acc: number, item: StructureCategoryResponse) => acc + item.percentile, 0) / 10;
      this.isLoading = false;
    },
    async makeParams() {
      return {
        set: [
          {
            cols: 9,
            key: "category_id",
            rules: [
              "required",
            ],
            title: t("categories.1"),
            type: "autocomplete",
            value: (await dsCategories.getAll())
              .map((a: Category) => ({
                value: a.category_id,
                title: a.category_name,
                selected: this.dialog.id && this.dialog.item.category_id === a.category_id,
              })),
          },
          {
            key: "percentile",
            cols: 3,
            rules: [
              "required",
              "number",
              ["value_range", 1, 99],
            ],
            title: t("portfolio.target_percent"),
            type: "number",
            value: !!this.dialog.id ? (this.dialog.item.percentile / 10) : "",
          },
        ],
      };
    },
    save(data: any) {
      this.isSaving = true;
      const result = {
        category_id: this.dialog.item.category_id,
        percentile: this.dialog.item.percentile,
        structure_id: this.dialog.item.structure_id,
      } as any;
      const gv = (a: any) => Array.isArray(a.value) ? a.value.find((item: any) => item.selected).value ?? null : a.value;

      Object.entries(data).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          for (const item of value) {
            result[item.key] = gv(item);
          }
        } else {
          result[key] = gv(value);
        }
      });
      result.percentile = Math.round(result.percentile * 10);
      result.structure_id = this.structure_id;
      if (this.dialog.id) {
        this.update(result);
      } else {
        this.add(result);
      }
      this.isSaving = false;
    },
    async setAsDefault() {
      const s = this.categories.reduce((acc: number, item: StructureCategoryResponse) => acc + item.percentile, 0);
      if (s !== 1000) {
        this.info = {
          color: "error",
          show: true,
          text: t("messages.less_100_percents", s / 10),
        }
        return;
      }
      try {
        await ds.set_structure_as_default(this.structure_id as number);
        this.loadData();
        this.info = {
          show: true,
          text: t("messages.structure_now_is_current"),
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
    async update(item: StructureCategory) {
      try {
        await ds.update(this.structure_id as number, item);
        this.loadCategories();
        this.close();
        this.info = {
          show: true,
          text: t("messages.updated"),
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
  },
  mounted() {
    state.settings[pageKey] = loadParams(pageKey) || state.settings[pageKey];
    state.refreshCallbacks[pageKey] = this.loadData;
    this.loadData();
  },
});
</script>
