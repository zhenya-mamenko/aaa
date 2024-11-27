export interface Messages {
  [key: string]: string;
}

export interface LocaleMessages {
  [language: string]: any;
}

export interface SettingsColumn {
  key: string;
  visible: boolean;
  disabled?: boolean;
  title: string;
}

export interface Settings {
  columns?: SettingsColumn[];
  [key: string]: any;
}

export interface SettingsMap {
  [key: string]: Settings;
}

export interface State {
  currencyPosition: string;
  currencySymbol: string;
  locale: string;
  messages: Messages;
  settings: {
    [key: string]: Settings;
  }
  refreshCallbacks: {
    [key: string]: Function;
  }
  theme: string;
}

export interface AppElement {
  component?: any;
  icon?: string;
  key: string;
  title: string;
  type: string;
}

export interface Rule {
  [key: string]: Function;
}
