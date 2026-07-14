/**
 * Tipo de documento de identidad aceptado por el backend.
 */
export type TipoDocumento = "CC" | "TI" | "CE" | "PA";

/**
 * Género del paciente.
 */
export type Genero = "Masculino" | "Femenino"  | "Prefiere no informar";

/**
 * Nivel de prioridad del paciente.
 */
export type Prioridad = "Alta" | "Media" | "Baja";

/**
 * Estado del paciente en el sistema.
 */
export type EstadoPaciente = "Pendiente" | "En atención" | "Atendido";

/**
 * Modelo completo de paciente tal como lo devuelve el backend (PatientResponse).
 * 15 campos según el nuevo modelo del backend.
 */
export interface Patient {
  paciente_id: number;
  tipo_documento: TipoDocumento;
  documento: string;
  nombre_completo: string;
  fecha_nacimiento: string; // ISO date "YYYY-MM-DD"
  genero: Genero;
  telefono: string;
  correo: string | null;
  eps_codigo: string;
  eps_nombre: string;
  ciudad: string | null;
  prioridad: Prioridad;
  estado: EstadoPaciente;
  fecha_creacion: string;      // ISO datetime
  fecha_actualizacion: string; // ISO datetime
}

/**
 * Payload para crear un paciente (PatientCreate).
 * Campos requeridos por el backend; opcionales marcados con ?.
 */
export interface PatientCreate {
  tipo_documento: TipoDocumento;
  documento: string;
  nombre_completo: string;
  fecha_nacimiento: string;
  genero: Genero;
  telefono: string;
  correo?: string;
  eps_codigo: string;
  eps_nombre: string;
  ciudad?: string;
  prioridad: Prioridad;
  estado: EstadoPaciente;
}

/**
 * Payload para actualizar un paciente (PatientUpdate).
 * Todos los campos son opcionales; solo se envían los que cambian.
 */
export interface PatientUpdate {
  tipo_documento?: TipoDocumento;
  documento?: string;
  nombre_completo?: string;
  fecha_nacimiento?: string;
  genero?: Genero;
  telefono?: string;
  correo?: string | null;
  eps_codigo?: string;
  eps_nombre?: string;
  ciudad?: string | null;
  prioridad?: Prioridad;
  estado?: EstadoPaciente;
}
