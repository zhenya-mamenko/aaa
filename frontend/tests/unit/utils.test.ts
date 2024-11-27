import { reactive } from "vue";
import '../localStorageMock';
import {
  calculateRebalancing, calculateReplenishment,
  isPlainObject, flattenObject,
  loadParams, saveParams, deleteParams,
  removeReactivity,
  findElement,
  format,
  parseAxiosError,
// @ts-ignore
} from "@/common/utils";


jest.mock("@/common/const", () => ({
  elements: [
    { key: "a", value: 1 },
    { key: "b", value: 2 },
    { key: "c", value: 3 },
  ],
}));


describe("Utils functions", () => {

  describe("Portfolio calculates", () => {

    test("Calculate Replenishment", () => {
      const list = [
        { structure_percentile: 200, calculated: 0 },
        { structure_percentile: 450, calculated: 0 },
        { structure_percentile: 350, calculated: 0 },
      ];
      calculateReplenishment(list, 1000);
      expect(list).toEqual([
        { structure_percentile: 200, calculated: 200 },
        { structure_percentile: 450, calculated: 450 },
        { structure_percentile: 350, calculated: 350 },
      ]);
    });

    test("Calculate Rebalancing", () => {
      const list = [
        { amount: 35000, structure_percentile: 200, calculated: 0 },
        { amount: 45000, structure_percentile: 450, calculated: 0 },
        { amount: 20000, structure_percentile: 350, calculated: 0 },
      ];

      calculateRebalancing(list, 0);
      expect(list).toEqual([
        { amount: 35000, structure_percentile: 200, calculated: -150 },
        { amount: 45000, structure_percentile: 450, calculated: 0 },
        { amount: 20000, structure_percentile: 350, calculated: 150 },
      ]);

      calculateRebalancing(list, 1000);
      expect(list).toEqual([
        { amount: 35000, structure_percentile: 200, calculated: 50 },
        { amount: 45000, structure_percentile: 450, calculated: 450 },
        { amount: 20000, structure_percentile: 350, calculated: 500 },
      ]);
    });

  });


  describe("Working with objects", () => {

    test("Check object is plain object", () => {
      const obj = { a: 1, b: 2, c: 3 };
      const resultObj = isPlainObject(obj);
      expect(resultObj).toBe(true);

      const arr = [1, 2, 3];
      const resultArr = isPlainObject(arr);
      expect(resultArr).toBe(false);

      const str = "string";
      const resultStr = isPlainObject(str);
      expect(resultStr).toBe(false);
    });

    test("Flatten object", () => {
      const obj = {
        a: 1,
        b: {
          c: 2,
          d: {
            e: 3,
            f: {
              g: 4,
            },
          },
        },
      };
      const resultObj = flattenObject(obj);
      expect(resultObj).toEqual({
        a: 1,
        "b.c": 2,
        "b.d.e": 3,
        "b.d.f.g": 4,
      });
    });

  });


  describe("Working with localStorage params", () => {

    test("Save Params", () => {
      const key = "testKey";
      const value = { a: 1, b: 2 };
      saveParams(key, value);

      const item = localStorage.getItem(key);
      expect(item).not.toBeNull();

      const savedValue = JSON.parse(item as string);
      expect(savedValue).toEqual(value);
    });

    test("Load Params", () => {
      const key = "testKey";
      const value = { a: 1, b: 2 };
      localStorage.setItem(key, JSON.stringify(value));
      const loadedValue = loadParams(key);

      expect(loadedValue).not.toBeNull();

      expect(loadedValue).toEqual(value);

      localStorage.removeItem(key);
      const nullValue = loadParams(key);
      expect(nullValue).toBeNull();
    });

    test("Delete Params", () => {
      const key = "testKey";
      localStorage.setItem(key, JSON.stringify({ a: 1, b: 2 }));
      deleteParams(key);

      const deletedValue = localStorage.getItem(key);
      expect(deletedValue).toBeNull();
    });

  });


  test("Remove reactivity", () => {
    const obj = reactive({ a: 1, b: 2, c: 3 });
    const resultObj = removeReactivity(obj);
    expect(resultObj).toEqual({ a: 1, b: 2, c: 3 });
  });


  test("Find element", () => {
    const resultElement = findElement("b");
    expect(resultElement).toEqual({ key: "b", value: 2 });
  });


  test("Format string", () => {
    const str = "Hello, {name}!";
    const resultStr = format(str, { name: "world" });
    expect(resultStr).toBe("Hello, world!");

    const str2 = "Hello!";
    const resultStr2 = format(str2);
    expect(resultStr2).toBe("Hello!");

    const str3 = "{0}, {1}!";
    const resultStr3 = format(str3, "Hello", "world");
    expect(resultStr3).toBe("Hello, world!");

  });


  test("Parse Axios Error", () => {
    const error1 = {
      response: {
        data: {
        },
      },
    };
    const result1 = parseAxiosError(error1);
    expect(result1).toBe("messages.backend.unknown_error");

    const error2 = {
      response: {
        data: {},
      },
      message: "error.message",
    };
    const result2 = parseAxiosError(error2);
    expect(result2).toBe("error.message");

    const error3 = {
      data: {},
    };
    const result3 = parseAxiosError(error3);
    expect(result3).toBe("messages.backend.no_reponse");

    const error4 = {
      response: {
        data: {
          detail: "",
        },
        status: 400,
      },
    };
    const result4 = parseAxiosError(error4);
    expect(result4).toStrictEqual([
      "messages.backend.request_error",
      400,
      "",
    ]);

    const error5 = {
      response: {
        data: {
          detail: "more detail",
        },
        status: 500,
      },
    };
    const result5 = parseAxiosError(error5);
    expect(result5).toStrictEqual([
      "messages.backend.request_error",
      500,
      "messages.backend.more_detail",
    ]);

    const error6 = {
      response: {
        data: {
          detail: "detail: test data",
        },
        status: 200,
      },
    };
    const result6 = parseAxiosError(error6);
    expect(result6).toStrictEqual([
      "messages.backend.request_error",
      200,
      "messages.backend.detail",
    ]);

  });

});
