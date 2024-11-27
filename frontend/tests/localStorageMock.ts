const localStorageMock = (() => {
  let store: { [key: string]: string } = {};

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => delete store[key],
  };
})();

const isNode = new Function("try {return this===global;}catch(e){return false;}");
if (isNode()) {
  Object.defineProperty(global, "localStorage", { value: localStorageMock, });
} else {
  Object.defineProperty(window, "localStorage", { value: localStorageMock, });
}
