import mockAxios from "jest-mock-axios";
// @ts-ignore
import ds from "@/services/CategoriesDataService";

jest.mock("axios", () => mockAxios);

describe("Categories DataService", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get all categories", async () => {
    const data = [
      { category_id: 1, class_id: 1, class_name: "Class 1", category_name: "Category 1" },
      { category_id: 2, class_id: 2, class_name: "Class 2", category_name: "Category 2" }
    ];
    const promise = ds.getAll();
    mockAxios.mockResponseFor({ method: "GET", url: "/categories" }, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get category by id", async () => {
    const data = { category_id: 1, class_id: 1, class_name: "Class 1", category_name: "Category 1" };
    const promise = ds.get(1);
    mockAxios.mockResponseFor({ method: "GET", url: "/categories/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create category", async () => {
    const data = { category_id: 1, class_id: 1, class_name: "Class 1", category_name: "Category 1" };
    const payload = { class_id: 1, category_name: "Category 1" };
    const promise = ds.create(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/categories" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update category", async () => {
    const data = { category_id: 1, class_id: 1, class_name: "Class 1", category_name: "Updated Category 1" };
    const payload = { class_id: 1, category_name: "Updated Category 1" };
    const promise = ds.update(1, payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/categories/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Delete category", async () => {
    const promise = ds.delete(1);
    mockAxios.mockResponseFor({ method: "DELETE", url: "/categories/1" }, );
    const result = await promise;
    expect(result).toBeUndefined();
  });

});
