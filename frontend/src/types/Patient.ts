/**
 * Tipo de documento de identidad aceptado por el backend.
 */
export type TipoDocumento = "CC" | "CE" | "TI" | "PA";

/**
 * Sexo biológico del paciente.
 */
export type Sexo = "M" | "F";

/**
 * Estado del paciente en el sistema.
 */
export type EstadoPaciente = "Activo" | "Inactivo";

/**
 * Modelo completo de paciente tal como lo devuelve el backend (PatientResponse).
 */
export interface Patient {
  id: number;
  tipo_documento: TipoDocumento;
  numero_documento: string;
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string; // ISO date "YYYY-MM-DD"
  sexo: Sexo;
  telefono: string;
  correo: string;
  direccion: string;
  estado: EstadoPaciente;
  fecha_creacion: string;   // ISO datetime
  fecha_actualizacion: string; // ISO datetime
}

/**
 * Payload para crear un paciente (PatientCreate).
 * Todos los campos son requeridos excepto los que el backend genera.
 */
export interface PatientCreate {
  tipo_documento: TipoDocumento;
  numero_documento: string;
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string;
  sexo: Sexo;
  telefono: string;
  correo: string;
  direccion: string;
  estado: EstadoPaciente;
}

/**
 * Payload para actualizar un paciente (PatientUpdate).
 * Todos los campos son opcionales; solo se envían los que cambian.
 */
export interface PatientUpdate {
  tipo_documento?: TipoDocumento;
  numero_documento?: string;
  nombres?: string;
  apellidos?: string;
  fecha_nacimiento?: string;
  sexo?: Sexo;
  telefono?: string;
  correo?: string;
  direccion?: string;
  estado?: EstadoPaciente;
}
