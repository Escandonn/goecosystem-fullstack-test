import { useState, type FormEvent } from "react";
import { Button } from "./Button";
import { Input } from "./Input";
import { Alert } from "./Alert";
import { useAuth } from "../hooks/useAuth";
import type { LoginFormData, LoginErrors } from "../types/Login";

export function LoginForm() {
  const { login, loading, error, setError } = useAuth();
  const [formData, setFormData] = useState<LoginFormData>({
    username: "",
    password: "",
  });
  const [errors, setErrors] = useState<LoginErrors>({});

  function validate(): boolean {
    const newErrors: LoginErrors = {};
    if (!formData.username.trim()) {
      newErrors.username = "El nombre de usuario es obligatorio";
    }
    if (!formData.password) {
      newErrors.password = "La contraseña es obligatoria";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (!validate()) return;
    await login(formData);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Limpiar error de ese campo al escribir
    if (errors[name as keyof LoginErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5" noValidate>
      {error && <Alert type="error" message={error} />}

      <Input
        label="Usuario"
        name="username"
        type="text"
        autoComplete="username"
        placeholder="Ingresa tu usuario"
        value={formData.username}
        onChange={handleChange}
        error={errors.username}
        disabled={loading}
      />

      <Input
        label="Contraseña"
        name="password"
        type="password"
        autoComplete="current-password"
        placeholder="Ingresa tu contraseña"
        value={formData.password}
        onChange={handleChange}
        error={errors.password}
        disabled={loading}
      />

      <Button type="submit" loading={loading} className="mt-2">
        {loading ? "Iniciando sesión…" : "Iniciar Sesión"}
      </Button>
    </form>
  );
}