import { type AppElement } from "@/types/common";
import { elements } from "@/common/const";


export const isPlainObject: Function = (o: any) => Boolean(
  o && o.constructor && o.constructor.prototype && o.constructor.prototype.hasOwnProperty("isPrototypeOf")
);


export const flattenObject: Function = (obj: any, keys = []) => {
  return Object.keys(obj).reduce((acc: any, key: any) => {
    return Object.assign(acc, isPlainObject(obj[key])
      ? flattenObject(obj[key], keys.concat(key))
      : { [keys.concat(key).join(".")]: obj[key] }
    )
  }, {})
}


export const loadParams: Function = (key: string) => {
  const savedParams = localStorage.getItem(key)
  if (savedParams) {
    return JSON.parse(savedParams)
  }
  return null
}


export const saveParams: Function = (key: string, params: any) => {
  localStorage.setItem(key, JSON.stringify(params))
}


export const deleteParams: Function = (key: string) => {
  localStorage.removeItem(key)
}


export const removeReactivity: Function = (o: any) => {
  return JSON.parse(JSON.stringify(o))
}

export const findElement: Function = (key: string): AppElement | undefined => {
  return elements.find((element: AppElement) => element.key === key);
}


// String.formatUnicorn polyfill from https://stackoverflow.com/a/18234317
export const format: Function = function(str: string, ...rest: any[]): string {
    if (rest.length) {
      var t = typeof rest[0];
      var key;
      var args = ("string" === t || "number" === t) ? Array.prototype.slice.call(rest) : rest[0];
      for (key in args) {
        str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
      }
    }
    return str;
  };


export const parseAxiosError: Function = (error: any): string | any[] => {
  if (error.response?.data?.detail !== undefined) {
    let message = "";
    const detail = error.response.data.detail;
    if (typeof detail === "string" && detail.length > 0) {
      message = `messages.backend.${detail.split(":")[0].replace(/ /g, "_")}`;
    }
    return [
      "messages.backend.request_error",
      error.response.status,
      message,
    ];
  } else if (!error.response) {
    return "messages.backend.no_reponse";
  } else {
    return error.message || "messages.backend.unknown_error";
  }
}


export const calculateReplenishment: Function = (
  list: any[],
  summa: number,
  percentileKey: string = "structure_percentile",
  resultKey: string = "calculated"
): void => {
  list.forEach(item => {
    (item as any)[resultKey] = Math.round(summa * item[percentileKey] / 1000);
  });
}


export const calculateRebalancing: Function = (
  list: any[],
  summa: number,
  amountKey: string = "amount",
  percentileKey: string = "structure_percentile",
  resultKey: string = "calculated"
): void => {
  const total = list.reduce((acc, item) => acc + item[amountKey], 0) + summa * 100;
  list.forEach(item => {
    (item as any)[resultKey] = Math.round(((total * item[percentileKey] / 1000) - item[amountKey]) / 100);
  });
}
