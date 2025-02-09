"use client";

import clsx from "clsx";
import { useFormStatus } from "react-dom";

interface FormSubmitButtonProps {
    label: string;
    text: string;
    pendingText: string;
}

export function FormSubmitButton({ label, text, pendingText }: FormSubmitButtonProps) {
    const { pending } = useFormStatus();
    return (
        <button type="submit" className={clsx(
            "inline-flex", "items-center", "justify-center",
            "px-2", "h-9",
            "bg-orange-700", "hover:bg-orange-800", "drop-shadow-box",
            "transition-colors"
        )} aria-label={label} aria-disabled={pending} disabled={pending}>
            {pending ? pendingText : text}
        </button>
    );
}
