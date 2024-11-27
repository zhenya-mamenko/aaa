import { type AppElement, type Settings, type SettingsMap } from "@/types/common";
import settings from "@/settings.json";


export const elements: AppElement[] = [
  {
    icon: "mdi-briefcase-variant",
    key: "portfolio",
    title: "portfolio.title",
    type: "page",
  },
  {
    icon: "mdi-finance",
    key: "assets_state",
    title: "assets.state",
    type: "page",
  },
  {
    icon: "mdi-invoice-text-clock",
    key: "statements",
    title: "assets.statements",
    type: "page",
  },
  {
    icon: "mdi-invoice-list",
    key: "assets",
    title: "assets.title",
    type: "dictionary",
  },
  {
    icon: "mdi-file-tree",
    key: "categories",
    title: "categories.title",
    type: "dictionary",
  },
  {
    icon: "mdi-shape-plus",
    key: "classes",
    title: "classes.title",
    type: "dictionary",
  },
  {
    icon: "mdi-list-box",
    key: "structures",
    title: "structures.title",
    type: "dictionary",
  },
  {
    icon: "mdi-label-percent",
    key: "structure_categories",
    title: "structures.assets",
    type: "complex_dictionary",
  },
  {
    icon: "mdi-cog",
    key: "settings",
    title: "settings.title",
    type: "dialog",
  },
]


export const defaultSettings: SettingsMap = {};
settings.forEach((setting) => {
  (defaultSettings as any)[setting.name] = setting.value as Settings;
});
