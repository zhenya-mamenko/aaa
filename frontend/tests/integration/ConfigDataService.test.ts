import mockAxios from "jest-mock-axios";
// @ts-ignore
import ds from "@/services/ConfigDataService";
import { tr } from "vuetify/locale";

jest.mock("axios", () => mockAxios);

describe("Config DataService", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get all config entries", async () => {
    const data = [
      { config_name: "config1", config_value: "value1" },
      { config_name: "config2", config_value: "value2" }
    ];
    const promise = ds.getAll();
    mockAxios.mockResponseFor({ method: "GET", url: "/config" }, { data: { data } });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Get config entry by name", async () => {
    const data = { config_name: "config1", config_value: "value1" };
    const promise = ds.get("config1");
    mockAxios.mockResponseFor({ method: "GET", url: "/config/config1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Create config entry", async () => {
    const data = { config_name: "config1", config_value: "value1" };
    const payload = { config_name: "config1", config_value: "value1" };
    const promise = ds.create(payload);
    mockAxios.mockResponseFor({ method: "POST", url: "/config" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update config entry", async () => {
    const data = { config_name: "config1", config_value: "updated_value1" };
    const payload = { config_name: "config1", config_value: "updated_value1" };
    const promise = ds.update("config1", payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/config/config1" }, { data });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Delete config entry", async () => {
    const promise = ds.delete("config1");
    mockAxios.mockResponseFor({ method: "DELETE", url: "/config/config1"});
    const result = await promise;
    expect(result).toBeUndefined();
  });

  test("Update or create: update if it exists", async () => {
    const data = { config_name: "config1", config_value: "value1" };
    const payload = { config_name: "config1", config_value: "value1" };

    const promise = ds.updateOrCreate(payload);
    mockAxios.mockResponseFor({ method: "PUT", url: "/config/config1" }, { data: payload });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

  test("Update or create: throw an error for non-404 error response", async () => {
    const payload = { config_name: "config1", config_value: "value1" };

    const promise = ds.updateOrCreate(payload);
    mockAxios.mockError({ response: { status: 500 }});

    await expect(promise).rejects.toEqual({ "isAxiosError": true, response: { status: 500 }});
    expect(mockAxios.post).not.toHaveBeenCalled();
  });

  test("Update or create: create if update fails with 404", async () => {
    const data = { config_name: "config1", config_value: "value1" };
    const payload = { config_name: "config1", config_value: "value1" };

    const promise = ds.updateOrCreate(payload);
    mockAxios.mockError({ response: { status: 404 }});
    mockAxios.useRequestHandler(async (req) => {
      mockAxios.mockResponse({ data }, req);
    });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

});
