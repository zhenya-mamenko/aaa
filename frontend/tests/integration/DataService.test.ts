import mockAxios from "jest-mock-axios";
// @ts-ignore
import ds from "@/services/DataService";

jest.mock("axios", () => mockAxios);

describe("Common DataService", () => {

  afterEach(() => {
    mockAxios.reset();
  });

  test("Get portfolio", async () => {
    const data = [
      {
        category_id: 1,
        class_name: "Class 1",
        category_name: "Category 1",
        structure_percentile: 10,
        out_structure_percentile: "10%",
        amount: 10000,
        out_amount: "$100.00",
        total: 50000,
        out_total: "$500.00",
        current_percentile: 20,
        out_current_percentile: "20%"
      },
      {
        category_id: 2,
        class_name: "Class 2",
        category_name: "Category 2",
        structure_percentile: 15,
        out_structure_percentile: "15%",
        amount: 20000,
        out_amount: "$200.00",
        total: 100000,
        out_total: "$1000.00",
        current_percentile: 25,
        out_current_percentile: "25%"
      }
    ];
    const promise = ds.getPortfolio();
    mockAxios.mockResponseFor({ method: "GET", url: "/portfolio" }, { data: { data} });
    const result = await promise;
    expect(result).toStrictEqual(data);
  });

});
