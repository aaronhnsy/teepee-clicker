import { clsx } from "clsx";

interface FormTextInputProps {
    type: `text` | `password`;
    label: string;
    fieldName: string;
}

export function FormTextInput({ type, label, fieldName }: FormTextInputProps) {
    return (
        <label className={clsx("flex", "flex-col", "items-stretch", "justify-start", "space-y-0.5")}>
            <p className={clsx("truncate", "text-xl", "font-bold")}>
                {label}
            </p>
            <input type={type} name={fieldName} className={clsx(
                "px-2", "h-9",
                "text-xl", "font-bold",
                "bg-orange-700", "hover:bg-orange-800", "drop-shadow-box",
                "transition-colors"
            )}/>
        </label>
    );
}
