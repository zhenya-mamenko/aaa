import api from "@/common/apiClient";
import { type Category, type CategoryResponse } from "@/types/Categories";


class CategoriesDataService {
  async getAll(): Promise<CategoryResponse[]> {
    return (await api.get("/categories")).data;
  }

  get(id: number): Promise<CategoryResponse> {
    return api.get(`/categories/${id}`);
  }

  create(data: Category): Promise<CategoryResponse> {
    return api.post("/categories", data);
  }

  update(id: number, data: Category): Promise<CategoryResponse> {
    return api.put(`/categories/${id}`, data);
  }

  delete(id: number): Promise<void> {
    return api.delete(`/categories/${id}`);
  }
}


export default new CategoriesDataService();
