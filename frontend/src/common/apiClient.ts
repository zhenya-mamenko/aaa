import axios from "axios";
import { type AxiosInstance } from "axios";


interface ApiResponse {
  data: any;
}

/* istanbul ignore next */
const API_URL = import.meta.env?.VITE_AAA_API_URL || "http://localhost:3000";


export class ApiClient {
  _client: AxiosInstance;

  constructor() {
    this._client = axios.create({
      baseURL: API_URL,
      headers: {
        "Content-type": "application/json",
      },
    });
  }

  async get(url: string, config?: any): Promise<any> {
    const result: ApiResponse = await this._client.get(url, config);
    return result.data;
  }

  async post(url: string, data: any, config?: any): Promise<any> {
    const result: ApiResponse = await this._client.post(url, data, config);
    return result.data;
  }

  async put(url: string, data: any, config?: any): Promise<any> {
    const result: ApiResponse = await this._client.put(url, data, config);
    return result.data;
  }

  async delete(url: string, config?: any): Promise<void> {
      await this._client.delete(url, config);
  }

  async patch(url: string, data?: any, config?: any): Promise<any> {
    const result: ApiResponse = await this._client.patch(url, data, config);
    return result.data;
  }

}

export default new ApiClient();
