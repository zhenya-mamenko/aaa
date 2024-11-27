import api from "@/common/apiClient";
import { type Class, type ClassResponse } from "@/types/Classes";


class ClassesDataService {
  async getAll(): Promise<ClassResponse[]> {
      return (await api.get("/classes")).data;
  }

  get(id: number): Promise<ClassResponse> {
    return api.get(`/classes/${id}`);
  }

  create(data: Class): Promise<ClassResponse> {
    return api.post("/classes", data);
  }

  update(id: number, data: Class): Promise<ClassResponse> {
    return api.put(`/classes/${id}`, data);
  }

  delete(id: number): Promise<void> {
    return api.delete(`/classes/${id}`);
  }

}


export default new ClassesDataService();
