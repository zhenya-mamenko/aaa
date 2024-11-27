import api from "@/common/apiClient";
import { type ConfigEntry } from "@/types/Config";


class ConfigDataService {
  async getAll(): Promise<ConfigEntry[]> {
    return (await api.get("/config")).data;
  }

  get(config_name: string): Promise<ConfigEntry> {
    return api.get(`/config/${config_name}`);
  }

  create(data: ConfigEntry): Promise<ConfigEntry> {
    return api.post("/config", data);
  }

  update(config_name: string, data: ConfigEntry): Promise<ConfigEntry> {
    return api.put(`/config/${config_name}`, data);
  }

  delete(config_name: string): Promise<void> {
    return api.delete(`/config/${config_name}`);
  }

  async updateOrCreate(data: ConfigEntry): Promise<ConfigEntry> {
    const config_name = data.config_name;
    try {
      return await this.update(config_name as string, data);
    } catch (error: any) {
      if (error.response.status === 404) {
        return await this.create(data);
      } else {
        throw error;
      }
    }
  }
}


export default new ConfigDataService();
