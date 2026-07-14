interface AlertProps {
  type?: "error" | "warning" | "info" | "success";
  message: string;
}

export function Alert({ type = "error", message }: AlertProps) {
  const styles = {
    error: "bg-red-50 border-red-400 text-red-700",
    warning: "bg-yellow-50 border-yellow-400 text-yellow-700",
    info: "bg-blue-50 border-blue-400 text-blue-700",
    success: "bg-green-50 border-green-400 text-green-700",
  };
  const icons = {
    error: "⚠",
    warning: "⚠",
    info: "ℹ",
    success: "✓",
  };

  return (
    <div
      className={`flex items-center gap-2 px-4 py-3 rounded-lg border ${styles[type]} text-sm`}
      role="alert"
    >
      <span className="text-lg">{icons[type]}</span>
      <span>{message}</span>
    </div>
  );
}
