<template>
  <v-dialog
    max-width="700px"
    :persistent="true"
    v-model="show"
  >
    <v-card
      class="pa-3"
    >
      <v-card-title
        class="ms-2"
        v-html="title"
      />
      <v-card-text>
        <v-form
          class="ma-0 pa-0"
          v-model="isValid"
        >
          <v-container class="ma-0 pa-0">
            <v-row
              v-for="item in results"
              :key="Array.isArray(item) ? (item as Array<any>)[0].title : item.title"
            >
              <v-col
                class="pt-1 pb-1 a"
                cols="12"
                :md="item.cols || (Array.isArray(item) && (item as Array<any>).length > 1 ? ((item as Array<any>)[0].cols || 6) : 12)"
              >
                <form-item
                  :params="Array.isArray(item) ? (item as Array<any>)[0] : item"
                />
              </v-col>
              <v-col v-if="Array.isArray(item) && (item as Array<any>).length > 1"
                class="pt-1 pb-1 b"
                cols="12"
                :md="(item as Array<any>)[1].cols || 6"
              >
                <form-item
                  :params="(item as Array<any>)[1]"
                />
              </v-col>
            </v-row>
            <v-row v-if="columns !== null && Object.keys(results).length > 0">
              <v-col>
                <v-divider class="mt-1 mb-1" />
              </v-col>
            </v-row>
            <v-row v-if="columns !== null">
              <v-col
                class="d-none d-md-inline text-h6"
                cols="3"
              >
                {{ t("settings.columns") }}
              </v-col>
              <v-col>
                <draggable
                  item-key="key"
                  v-model="columns"
                >
                  <template #item="{element}">
                    <div
                      class="border pa-1 ps-3 mb-1 rounded-lg bg-primary-lighten-5"
                      :key="element.title"
                    >
                      <v-switch
                        color="primary"
                        :data-testid="`switch-${element.title}`"
                        density="comfortable"
                        :disabled="element.disabled"
                        :hide-details="true"
                        inset
                        :label="t(element.title)"
                        v-model="element.visible"
                      ></v-switch>
                    </div>
                  </template>
                </draggable>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions
        class="pe-4 me-2"
      >
        <v-btn v-if="showResetButton"
          data-testid="form-dialog-reset-button"
          @click="reset"
        >
          <v-icon class="d-inline-block d-md-none" size="x-large">mdi-cog-refresh</v-icon>
          <span class="d-none d-md-inline-block">{{ t("buttons.reset") }}</span>
        </v-btn>
        <v-spacer />
        <v-btn
          color="primary"
          data-testid="form-dialog-save-button"
          :disabled="!isValid"
          @click="save"
        >
          {{ t("buttons.save") }}
        </v-btn>
        <v-btn
          @click="closeDialog"
        >
          {{ t("buttons.close") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import draggable from "vuedraggable";
import { t } from "@/common/locale";
import { type SettingsColumn, type Settings } from "@/types/common";
import FormItem from "./FormItem.vue";
import { removeReactivity } from '@/common/utils';


export default defineComponent({
  name: "FormDialog",
  components: {
    draggable,
    FormItem,
  },
  data() {
    return {
      isValid: true as boolean,
      columns: [] as SettingsColumn[],
      results: {} as Settings,
      show: false as boolean,
    };
  },
  computed: {
    t() {
      return t;
    },
  },
  emits: [
    "close",
    "reset",
    "save",
  ],
  methods: {
    closeDialog() {
      this.$emit("close");
    },
    parseParams(newValue: Settings) {
      this.columns = !!newValue.columns ? removeReactivity(newValue.columns) : null;
      this.results = Object.fromEntries(
        Object.entries(removeReactivity(newValue)).filter(
          ([key, value]) => key !== "columns" && ((value as any).value !== undefined || Array.isArray(value))
            && (!(value as any).type || (value as any).type !== "hidden")
        )
      );
    },
    reset() {
      this.$emit("reset");
    },
    save() {
      const fe = (res: any, old: any) => {
        return Object.fromEntries(
          Object.entries(res).map(
            ([key, value]) => {
              const p = old[key] as any;
              if (Array.isArray(value)) {
                value = value.map((item: any, index: number) => {
                  return fe(item, p[index]);
                });
              } else if (typeof value === "object") {
                (value as any).title = p.title;
              } else if (key === "title") {
                value = old[key];
              }
              return [key, value];
            }
          )
        )
      }
      const results = {...this.params, ...fe(this.results, this.params)};
      if (this.columns) {
        results.columns = this.columns;
      }
      this.$emit("save", results);
    },
  },
  mounted() {
    this.parseParams(this.params);
  },
  props: {
    title: {
      type: String,
      required: false,
    },
    opened: {
      type: Boolean,
      required: true,
    },
    params: {
      type: Object as () => Settings,
      required: true,
    },
    showResetButton: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  watch: {
    opened(newValue: boolean) {
      this.show = newValue;
    },
    params(newValue) {
      this.parseParams(newValue);
    },
  },
});
</script>
