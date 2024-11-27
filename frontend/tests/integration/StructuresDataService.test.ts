import mockAxios from "jest-mock-axios";
// @ts-ignore
import ds from "@/services/StructuresDataService";

jest.mock("axios", () => mockAxios);

describe("Structures DataService", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get all structures", async () => {
    const data = [
      { structure_id: 1, structure_date: "2023-01-01", structure_name: "Structure 1", is_current: true },
      { structure_id: 2, structure_date: "2023-01-02", structure_name: "Structure 2", is_current: false }
    ];
    const promise = ds.getAll();
    mockAxios.mockResponseFor({ method: "GET", url: "/structures" }, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get all categories for a structure", async () => {
    const data = [
      { structure_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", percentile: 50 },
      { structure_id: 1, category_id: 2, class_name: "Class 2", category_name: "Category 2", percentile: 50 }
    ];
    const promise = ds.getAll(1);
    mockAxios.mockResponseFor({ method: "GET", url: "/structures/1/categories" }, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get structure by id", async () => {
    const data = { structure_id: 1, structure_date: "2023-01-01", structure_name: "Structure 1", is_current: true };
    const promise = ds.get(1);
    mockAxios.mockResponseFor({ method: "GET", url: "/structures/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get category by id for a structure", async () => {
    const data = { structure_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", percentile: 50 };
    const promise = ds.get(1, 1);
    mockAxios.mockResponseFor({ method: "GET", url: "/structures/1/categories/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create structure", async () => {
    const data = { structure_id: 1, structure_date: "2023-01-01", structure_name: "Structure 1", is_current: true };
    const payload = { structure_date: "2023-01-01", structure_name: "Structure 1", is_current: true };
    const promise = ds.create(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/structures" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create category for a structure", async () => {
    const data = { structure_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", percentile: 50 };
    const payload = { structure_id: 1, category_id: 1, percentile: 50 };
    const promise = ds.create(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/structures/1/categories" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update structure", async () => {
    const data = { structure_id: 1, structure_date: "2023-01-01", structure_name: "Updated Structure 1", is_current: true };
    const payload = { structure_date: "2023-01-01", structure_name: "Updated Structure 1", is_current: true };
    const promise = ds.update(1, payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/structures/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update category for a structure", async () => {
    const data = { structure_id: 1, category_id: 1, class_name: "Class 1", category_name: "Updated Category 1", percentile: 60 };
    const payload = { structure_id: 1, category_id: 1, percentile: 60 };
    const promise = ds.update(1, payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/structures/1/categories/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Delete structure", async () => {
    const promise = ds.delete(1);
    mockAxios.mockResponseFor({ method: "DELETE", url: "/structures/1" });
    const result = await promise;
    expect(result).toBeUndefined();
  });

  test("Delete category for a structure", async () => {
    const promise = ds.delete(1, 1);
    mockAxios.mockResponseFor({ method: "DELETE", url: "/structures/1/categories/1" });
    const result = await promise;
    expect(result).toBeUndefined();
  });

  test("Set structure as default", async () => {
    const data = { structure_id: 1, structure_date: "2023-01-01", structure_name: "Structure", is_current: true };
    const promise = ds.set_structure_as_default(1);
    mockAxios.mockResponseFor({ method: "PATCH", url: "/structures/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

});
