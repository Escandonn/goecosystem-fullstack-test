import { api } from "./api";
import type { Patient, PatientCreate, PatientUpdate } from "../types/Patient";

/**
 * Servicio de pacientes.
 * Consume los endpoints reales de FastAPI en /api/v1/pacientes.
 * El Bearer token es inyectado automáticamente por el interceptor de api.ts.
 */
export const patientService = {
  /**
   * GET /pacientes?skip=&limit=
   * Obtiene la lista paginada de todos los pacientes.
   */
  async getAll(skip = 0, limit = 100): Promise<Patient[]> {
    const response = await api.get<Patient[]>("/pacientes", {
      params: { skip, limit },
    });
    return response.data;
  },

  /**
   * GET /pacientes/search?q=&skip=&limit=
   * Busca pacientes por nombre, apellido o número de documento.
   */
  async search(q: string, skip = 0, limit = 100): Promise<Patient[]> {
    const response = await api.get<Patient[]>("/pacientes/search", {
      params: { q, skip, limit },
    });
    return response.data;
  },

  /**
   * GET /pacientes/count
   * Retorna el total de pacientes registrados.
   */
  async count(): Promise<number> {
    const response = await api.get<{ total: number }>("/pacientes/count");
    return response.data.total;
  },

  /**
   * GET /pacientes/{paciente_id}
   * Obtiene un paciente por su ID.
   */
  async getById(paciente_id: number): Promise<Patient> {
    const response = await api.get<Patient>(`/pacientes/${paciente_id}`);
    return response.data;
  },

  /**
   * POST /pacientes
   * Crea un nuevo paciente. Retorna 201 con el paciente creado.
   */
  async create(data: PatientCreate): Promise<Patient> {
    const response = await api.post<Patient>("/pacientes", data);
    return response.data;
  },

  /**
   * PUT /pacientes/{paciente_id}
   * Actualiza los campos enviados de un paciente existente.
   */
  async update(paciente_id: number, data: PatientUpdate): Promise<Patient> {
    const response = await api.put<Patient>(`/pacientes/${paciente_id}`, data);
    return response.data;
  },

  /**
   * DELETE /pacientes/{paciente_id}
   * Elimina un paciente (solo admin). Retorna 204 sin contenido.
   */
  async delete(paciente_id: number): Promise<void> {
    await api.delete(`/pacientes/${paciente_id}`);
  },
};
