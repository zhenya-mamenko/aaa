import mockAxios from "jest-mock-axios";
// @ts-ignore
import ds from "@/services/AssetsDataService";

jest.mock("axios", () => mockAxios);

describe("Assets DataService", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get all assets", async () => {
    const data = [
      { asset_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Asset 1", asset_ticker: "TICK1" },
      { asset_id: 2, category_id: 2, class_name: "Class 2", category_name: "Category 2", asset_name: "Asset 2", asset_ticker: "TICK2" }
    ]
    const promise = ds.getAll();
    mockAxios.mockResponseFor({ method: "GET", url: "/assets"}, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get asset by id", async () => {
    const data = { asset_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Asset 1", asset_ticker: "TICK1" };
    const promise = ds.get(1);
    mockAxios.mockResponseFor({ method: "GET", url: "/assets/1"}, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create asset", async () => {
    const data = { asset_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Asset 1", asset_ticker: "TICK1" };
    const payload = { category_id: 1, asset_name: "Asset 1", asset_ticker: "TICK1" }
    const promise = ds.create(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/assets"}, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update asset", async () => {
    const data = { asset_id: 1, category_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Updated Asset 1", asset_ticker: "TICK1" };
    const payload = { category_id: 1, asset_name: "Updated Asset 1", asset_ticker: "TICK1" };
    const promise = ds.update(1, payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/assets/1"}, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Delete asset", async () => {
    const promise = ds.delete(1);
    mockAxios.mockResponseFor({ method: "DELETE", url: "/assets/1"});
    const result = await promise;
    expect(result).toBeUndefined();
  });

  test("Get assets state", async () => {
    const data =  [
      { asset_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Asset 1", asset_ticker: "TICK1", last: 100, lag: 90, first: 80, last_lag_percent: 11.11, last_first_percent: 25, lag_first_percent: 12.5, out_last: "1.00", out_lag: "0.90", out_first: "0.80", out_last_lag_percent: "11.11%", out_last_first_percent: "25%", out_lag_first_percent: "12.5%" },
      { asset_id: 2, class_name: "Class 2", category_name: "Category 2", asset_name: "Asset 2", asset_ticker: "TICK2", last: 200, lag: 180, first: 160, last_lag_percent: 11.11, last_first_percent: 25, lag_first_percent: 12.5, out_last: "2.00", out_lag: "1.80", out_first: "1.60", out_last_lag_percent: "11.11%", out_last_first_percent: "25%", out_lag_first_percent: "12.5%" }
    ]
    const promise = ds.getState();
    mockAxios.mockResponseFor({ method: "GET", url: "/assets/state"}, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get assets values", async () => {
    const data = [
      { asset_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Asset 1", asset_ticker: "TICK1", asset_value_datetime: "2023-01-01T00:00:00Z", amount: 100, out_amount: "1.00" },
      { asset_id: 2, class_name: "Class 2", category_name: "Category 2", asset_name: "Asset 2", asset_ticker: "TICK2", asset_value_datetime: "2023-01-02T00:00:00Z", amount: 200, out_amount: "2.00" }
    ]
    const promise = ds.getValues();
    mockAxios.mockResponseFor({ method: "GET", url: "/assets/values"}, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create asset value", async () => {
    const data = { asset_id: 1, class_name: "Class 1", category_name: "Category 1", asset_name: "Asset 1", asset_ticker: "TICK1", asset_value_datetime: "2023-01-01T00:00:00Z", amount: 100, out_amount: "1.00" };
    const payload = { asset_id: 1, amount: 100 };
    const promise = ds.createValue(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/assets/values"}, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

});
