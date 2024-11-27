import api from "@/common/apiClient";
import { type Asset, type AssetResponse, type AssetsStateResponse, type AssetsValuesResponse, type AssetValue } from "@/types/Assets";


class AssetsDataService {
  async getAll(): Promise<AssetResponse[]> {
    return (await api.get("/assets")).data;
  }

  async getState(): Promise<AssetsStateResponse[]> {
    return (await api.get("/assets/state")).data;
  }

  async getValues(): Promise<AssetsValuesResponse[]> {
    return (await api.get("/assets/values")).data;
  }

  get(id: number): Promise<AssetResponse> {
    return api.get(`/assets/${id}`);
  }

  create(data: Asset): Promise<AssetResponse> {
    return api.post("/assets", data);
  }

  createValue(data: AssetValue): Promise<AssetsValuesResponse> {
    return api.post("/assets/values", data);
  }

  update(id: number, data: Asset): Promise<AssetResponse> {
    return api.put(`/assets/${id}`, data);
  }

  delete(id: number): Promise<void> {
    return api.delete(`/assets/${id}`);
  }
}


export default new AssetsDataService();
