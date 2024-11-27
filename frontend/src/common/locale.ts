import { state } from "@/common/state";
import { flattenObject, format } from "@/common/utils";
import messages from "@/messages.json";
import { type Messages, type LocaleMessages } from "@/types/common";


export function setLocale(locale: string) {
  state.locale = locale;
  state.messages = flattenObject((messages as LocaleMessages)[locale]) as Messages;
}


export function t(key: string, ...rest: any): string {
  key = String(key);
  let text = state.messages[key];
  if (text === undefined) {
    const parts = key.split(".");
    text = parts[parts.length - 1].replace(/_/g, " ");
  }
  if (rest.length) {
    rest = rest.map((item: string) => t(item));
    text = format(text, ...rest);
  }
  return text;
}
