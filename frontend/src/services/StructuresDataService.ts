
import api from "@/common/apiClient";
import { type Structure, type StructureResponse, type StructureCategory, type StructureCategoryResponse } from "@/types/Structures";


class StructuresDataService {
  async getAll(structure_id?: number): Promise<StructureResponse[] | StructureCategoryResponse[]>;
  async getAll(structure_id: number): Promise<StructureCategoryResponse[]> {
    return (await api.get(`/structures${structure_id ? `/${structure_id}/categories` : ""}`)).data;
  }

  get(structure_id: number, category_id?: number): Promise<StructureResponse | StructureCategoryResponse>;
  get(structure_id: number, category_id: number): Promise<StructureCategoryResponse> {
    return api.get(`/structures/${structure_id}${category_id ? `/categories/${category_id}` : ""}`);
  }

  create(data: Structure | StructureCategory): Promise<StructureResponse | StructureCategoryResponse> {
    if ("category_id" in data) {
      return api.post(`/structures/${data.structure_id}/categories`, data);
    }
    return api.post("/structures", data);
  }

  update(structure_id: number, data: Structure | StructureCategory): Promise<StructureResponse | StructureCategoryResponse> {
    if ("category_id" in data) {
      return api.put(`/structures/${structure_id}/categories/${(data as StructureCategory).category_id}`, data);
    }
    return api.put(`/structures/${structure_id}`, data);
  }

  delete(structure_id: number, category_id?: number): Promise<void> {
    return api.delete(`/structures/${structure_id}${category_id ? `/categories/${category_id}` : ""}`);
  }

  set_structure_as_default(structure_id: number): Promise<void> {
    return api.patch(`/structures/${structure_id}`);
  }

}


export default new StructuresDataService();
