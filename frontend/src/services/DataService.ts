import api from "@/common/apiClient";
import { type PortfolioResponse } from "@/types/Types";


class DataService {
  async getPortfolio(): Promise<PortfolioResponse[]> {
    const result = (await api.get("/portfolio")).data;
    return result;
  }
}


export default new DataService();
