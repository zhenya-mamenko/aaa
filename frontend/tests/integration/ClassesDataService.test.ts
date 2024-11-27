import mockAxios from "jest-mock-axios";
// @ts-ignore
import ds from "@/services/ClassesDataService";

jest.mock("axios", () => mockAxios);

describe("Classes DataService", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get all classes", async () => {
    const data = [
      { class_id: 1, class_name: "Class 1" },
      { class_id: 2, class_name: "Class 2" }
    ];
    const promise = ds.getAll();
    mockAxios.mockResponseFor({ method: "GET", url: "/classes" }, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get class by id", async () => {
    const data = { class_id: 1, class_name: "Class 1" };
    const promise = ds.get(1);
    mockAxios.mockResponseFor({ method: "GET", url: "/classes/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create class", async () => {
    const data = { class_id: 1, class_name: "Class 1" };
    const payload = { class_name: "Class 1" };
    const promise = ds.create(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/classes" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update class", async () => {
    const data = { class_id: 1, class_name: "Updated Class 1" };
    const payload = { class_name: "Updated Class 1" };
    const promise = ds.update(1, payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/classes/1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Delete class", async () => {
    const promise = ds.delete(1);
    mockAxios.mockResponseFor({ method: "DELETE", url: "/classes/1" }, );
    const result = await promise;
    expect(result).toBeUndefined();
  });

});
