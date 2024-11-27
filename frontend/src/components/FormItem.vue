<template>
  <v-switch v-if="isBoolean"
    color="primary"
    density="comfortable"
    :data-testid="`switch-${params.title.replace(/\./g, '-').toLowerCase()}`"
    :hide-details="true"
    inset
    :label="t(params.title)"
    v-model="params.value"
  ></v-switch>
  <v-text-field v-else-if="isString || isNumber"
    :counter="isString && params.counter ? params.counter : false"
    :data-testid="`text-field-${params.title.replace(/\./g, '-').toLowerCase()}`"
    hide-spin-buttons
    :label="t(params.title)"
    persistent-hint
    :rules="rules"
    :type="inputType"
    v-model="params.value"
  ></v-text-field>
  <v-select v-else-if="isArray && !isAutoComplete"
    :data-testid="`select-${params.title.replace(/\./g, '-').toLowerCase()}`"
    :items="params.value.map((item: any) => {
      item.title = t(item.title)
      return item;
    })"
    :label="t(params.title)"
    v-model="selectedValue"
  ></v-select>
  <v-autocomplete v-else-if="isArray && isAutoComplete"
    auto-select-first
    :data-testid="`autocomplete-${params.title.replace(/\./g, '-').toLowerCase()}`"
    :items="params.value.map((item: any) => {
      item.title = t(item.title)
      return item;
    })"
    :label="t(params.title)"
    v-model="selectedValue"
  ></v-autocomplete>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { t } from "@/common/locale";
import { type Rule } from "@/types/common";


export const rules: Rule = {
  required: () => (v: any) => !!v || t("errors.required"),
  max_length: (max: number) => (v: any) => String(v).length <= max || t("errors.max_length", max),
  number: () => (v: any) => !isNaN(parseFloat(v)) || t("errors.number"),
  min_value: (min: number) => (v: any) => v >= min || t("errors.min_value", min),
  value_range: (min: number, max: number) => (v: any) => v >= min && v <= max || t("errors.value_range", min, max),
}

export default defineComponent({
  name: 'FormItem',
  computed: {
    isArray(): boolean {
      return Array.isArray(this.params.value);
    },
    isBoolean(): boolean {
      return typeof this.params.value === "boolean";
    },
    isDate(): boolean {
      return this.params.type === "date";
    },
    isNumber(): boolean {
      return this.params.type === "number" || typeof this.params.value === "number";
    },
    isString(): boolean {
      return typeof this.params.value === "string";
    },
    isAutoComplete(): boolean {
      return this.params.type === "autocomplete";
    },
    inputType(): string {
      if (this.isDate) return "date";
      return typeof this.params.value === "number" ? "number" : "text";
    },
    rules() {
      if (!this.params.rules) return [];
      const result = [];
      for (const rule of this.params.rules) {
        if (!Array.isArray(rule) && rules[rule]) {
          result.push(rules[rule]());
          continue;
        } else if (!rules[rule[0]]) {
          continue;
        }
        result.push(rules[rule[0]](...rule.slice(1)));
      }
      return result;
    },
    selectedValue: {
      get(): string {
        return this.params.value.find((item: any) => item.selected)?.value;
      },
      set(newValue: string) {
        const selectedItem = this.params.value.find((item: any) => item.value === newValue);
        if (selectedItem) {
          this.params.value.forEach((item: any) => item.selected = false);
          selectedItem.selected = true;
        }
      }
    },
    t() {
      return t;
    },
  },
  props: {
    params: {
      type: Object,
      required: true,
    },
  },
});
</script>
