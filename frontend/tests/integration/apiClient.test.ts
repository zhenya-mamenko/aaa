import mockAxios from "jest-mock-axios";
// @ts-ignore
import apiClient from "@/common/apiClient";


jest.mock("axios", () => mockAxios);


describe("API client", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get request", async () => {
    const promise = apiClient.get("/");
    mockAxios.mockResponse({ data: "data" });
    const result = await promise;
    expect(result).toBe("data");
  });

  test("Post request", async () => {
    const promise = apiClient.post("/", { data: "data" });
    mockAxios.mockResponse({ data: "data" });
    const result = await promise;
    expect(result).toBe("data");
  });

  test("Put request", async () => {
    const promise = apiClient.put("/", { data: "data" });
    mockAxios.mockResponse({ data: "data" });
    const result = await promise;
    expect(result).toBe("data");
  });

  test("Patch request", async () => {
    const promise = apiClient.patch("/", { data: "data" });
    mockAxios.mockResponse({ data: "data" });
    const result = await promise;
    expect(result).toBe("data");
  });

  test("Delete request", async () => {
    const promise = apiClient.delete("/");
    mockAxios.mockResponse();
    const result = await promise;
    expect(result).toBeUndefined();
  });

});
