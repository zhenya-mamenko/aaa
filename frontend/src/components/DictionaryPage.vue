<template>
  <v-data-table data-testid="dictionary-page-data-table"
    class="h-100"
    :headers="headers"
    :items="items"
    :loading="isLoading"
    :loading-text="t('messages.loading')"
    :search="search"
    sort-asc-icon="mdi-triangle-small-up"
    sort-desc-icon="mdi-triangle-small-down"
    :sticky="true"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-icon class="ms-3 me-3" size="large">
          {{ icon }}
        </v-icon>
        <v-toolbar-title class="d-none d-md-block ms-0">
          {{ `${t("dictionaries")}: ${title}` }}
        </v-toolbar-title>
        <v-responsive class="w-25">
          <v-text-field data-testid="dictionary-page-search-input"
            clearable clear-icon="mdi-close" density="compact" hide-details :label="t('search')"
            persistent-clear prepend-inner-icon="mdi-magnify" single-line v-model="search" />
        </v-responsive>
        <v-divider class="ms-3 me-3" vertical />
        <v-btn data-testid="dictionary-page-add-button"
          class="me-2"
          color="primary-darken-3"
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
  <v-snackbar data-testid="dictionary-page-snackbar"
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
import { findElement, loadParams, parseAxiosError, removeReactivity } from "@/common/utils";

import assetsDS from "@/services/AssetsDataService";
import categoriesDS from "@/services/CategoriesDataService";
import classesDS from "@/services/ClassesDataService";
import structuresDS from "@/services/StructuresDataService";
import { type AssetResponse, type Asset } from "@/types/Assets";
import { type CategoryResponse, type Category } from "@/types/Categories";
import { type ClassResponse, type Class } from "@/types/Classes";
import { type StructureResponse, type Structure } from '@/types/Structures';


type Response = AssetResponse | CategoryResponse | ClassResponse | StructureResponse;
type Item = Asset | Category | Class | Structure;


export default defineComponent({
  computed: {
    ds() {
      const list = {
        assets: assetsDS,
        categories: categoriesDS,
        classes: classesDS,
        structures: structuresDS,
      }
      return (list as any)[this.pageKey] || assetsDS;
    },
    headers() {
      const columns = this.params.columns;
      if (!columns) return [];
      const result = columns
        .filter(column => column.visible)
        .map(column => {
          let header = removeReactivity(column);
          header.align = "start";
          if (header.title === "id") {
            header = {...header, align: "right", maxWidth: "40px", width: "40px", };
          }
          header.title = t(header.title);
          if (header.type === "date") {
            header.value = (value: string) => (new Date((value as any).structure_date)).toLocaleDateString(state.locale);
            header = {...header, maxWidth: "90px", width: "90px", };
          } else if (header.type === "boolean") {
            header.value = (value: Boolean) => (value as any).is_current ?
              t("messages.yes").toLowerCase() : t("messages.no").toLowerCase();
            header = {...header, align: "center", maxWidth: "80px", width: "80px", };
          }
          return header;
        });
      result.push({ title: t("actions"), sortable: false, align: "center", maxWidth: "80px", width: "80px", value: "actions", });
      return result;
    },
    params() {
      return state.settings[this.pageKey];
    },
    t() {
      return t;
    },
  },
  data() {
    return {
      confirmationDialog: {
        id: 0 as number,
        item: {} as any,
        opened: false,
        text: "",
      },
      dialog: {
        id: null as number | null,
        item: {} as any,
        itemProps: [],
        opened: false,
        params: {},
        title: "",
      },
      icon: "",
      info: {
        color: "success",
        show: false,
        text: "",
        timeout: 2000,
      } as Partial<{ color: string, show: boolean, text: string, timeout: number }>,
      isLoading: false,
      isSaving: false,
      items: [] as Response[],
      title: "",
      search: "",
    }
  },
  methods: {
    close() {
      this.dialog.opened = false;
      this.dialog.item = {} as any;
      this.dialog.id = null;
    },
    async createItem() {
      this.dialog.title = t("buttons.add") + " " + t(this.pageKey + ".2").toLowerCase();
      this.dialog.params = await this.makeParams();
      this.dialog.opened = true;
    },
    async add(item: Item) {
      try {
        await this.ds.create(item);
        this.loadData();
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
    async confirmDelete(item: any) {
      this.confirmationDialog.text = t(
        "confirmations.delete_text", item.asset_name || item.category_name || item.class_name || item.structure_name
      );
      this.confirmationDialog.id = item.asset_id || item.category_id || item.class_id || item.structure_id;
      this.confirmationDialog.item = item;
      this.confirmationDialog.opened = true;
    },
    async deleteItem(id: number) {
      try {
        this.confirmationDialog.opened = false;
        await this.ds.delete(id);
        this.loadData()
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
    async editItem(item: any) {
      this.dialog.item = item as Item;
      this.dialog.id = item.asset_id || item.category_id || item.class_id || item.structure_id;
      this.dialog.params = await this.makeParams();
      this.dialog.title = t("buttons.edit") + " " + t(this.pageKey + ".2").toLowerCase();
      this.dialog.opened = true;
    },
    async loadData() {
      this.isLoading = true;
      this.title = t(findElement(this.pageKey).title);
      this.icon = findElement(this.pageKey).icon;
      if (this.ds) {
        const items = await this.ds.getAll();
        this.items = items;
      }
      this.isLoading = false;
    },
    makeItem(item: Item, data: any): Item {
      const result = {} as any;
      for (const key of this.dialog.itemProps) {
        result[key] = item[key];
      }
      const gv = (a: any) => Array.isArray(a.value) ? a.value.find((item: any) => item.selected).value ?? null : a.value;

      Object.entries(data).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          for (const item of value) {
            if (item.key in result) result[item.key] = gv(item);
          }
        } else if (key in result) {
          result[key] = gv(value);
        }
      });
      return result;
    },
    async makeParams() {
      const item = this.dialog.item as any;
      if (this.pageKey === "assets") {
        this.dialog.itemProps = ["asset_name", "category_id", "asset_id", "asset_ticker"] as any;
        return {
          asset_name: {
            rules: [
              "required",
              ["max_length", 200, ],
            ],
            title: "assets.1",
            value: item.asset_name || "",
          },
          set: [
            {
              cols: 9,
              key: "category_id",
              rules: [
                "required",
              ],
              title: "categories.1",
              type: "autocomplete",
              value: (await categoriesDS.getAll()).map((c: Category, index: number) => ({
                value: c.category_id,
                title: c.category_name,
                selected: !item.category_id ? null : c.category_id === item.category_id,
              })),
            },
            {
              cols: 3,
              counter: 10,
              key: "asset_ticker",
              rules: [
                ["max_length", 10, ],
              ],
              title: "assets.ticker",
              value: item.asset_ticker || "",
            },
          ],
        }
      } else if (this.pageKey === "categories") {
        this.dialog.itemProps = ["category_id", "class_id", "category_name"] as any;
        return {
          category_name: {
            rules: [
              "required",
              ["max_length", 100, ],
            ],
            title: "categories.1",
            value: item.category_name || "",
          },
          class_id: {
            rules: [
              "required",
            ],
            title: "classes.1",
            value: (await classesDS.getAll()).map((c: Class, index: number) => ({
              value: c.class_id,
              title: c.class_name,
              selected: !item.class_id ? index === 0 : c.class_id === item.class_id,
            })),
          },
        }
      } else if (this.pageKey === "classes") {
        this.dialog.itemProps = ["class_name", "class_id"] as any;
        return {
          class_name: {
            rules: [
              "required",
              ["max_length", 100, ],
            ],
            title: "classes.1",
            value: item.class_name || "",
          },
        }
      } else if (this.pageKey === "structures") {
        this.dialog.itemProps = ["structure_name", "structure_date", "is_current"] as any;
        return {
          set: [
            {
              cols: 8,
              key: "structure_name",
              rules: [
                "required",
                ["max_length", 100, ],
              ],
              title: "structures.1",
              value: item.structure_name || "",
            },
            {
              cols: 4,
              key: "structure_date",
              rules: [
                "required",
              ],
              title: "date.title",
              type: "date",
              value: !!item.structure_date ? 
                (new Date(item.structure_date)).toISOString().substring(0, 10) : (new Date()).toISOString().substring(0, 10),
            },
          ],
          is_current: {value: item.is_current || false, type: "hidden", },
        }
      }
      return {};
    },
    save(data: any) {
      this.isSaving = true;
      const item = this.makeItem(this.dialog.item, data);
      if (this.dialog.id) {
        this.update(this.dialog.id, item);
      } else {
        this.add(item);
      }
      this.isSaving = false;
    },
    async update(id: number, item: Item) {
      try {
        await this.ds.update(id, item);
        this.loadData();
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
    state.settings[this.pageKey] = loadParams(this.pageKey) || state.settings[this.pageKey];
    state.refreshCallbacks["this.pageKey"] = this.loadData;
    this.loadData();
  },
  props: {
    pageKey: {
      type: String,
      required: true,
    },
  },
  watch: {
    pageKey() {
      this.loadData();
    },
  },
});
</script>
