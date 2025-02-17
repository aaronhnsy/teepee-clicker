"use client";

import clsx from "clsx";
import React from "react";

interface ButtonProps {
    label: string;
    type?: `button` | `submit` | `reset`;
    disabled?: boolean;
    onClick?: (event?: React.MouseEvent) => void;
}

export function Button({ type, label, disabled, onClick }: ButtonProps) {
    return (
        <button type={type ?? "button"} aria-label={label} aria-disabled={disabled} disabled={disabled}
                onClick={onClick} className={clsx(
                    "inline-flex", "items-center", "justify-center", "text-center",
                    "p-2",
                    "text-black", "text-base", "font-medium",
                    "bg-orange-600", "hover:bg-orange-700", "active:bg-orange-700", "focus:bg-orange-700",
                    "hover:translate-0.25", "active:translate-0.25", "focus:translate-0.25",
                    "transition-all", "drop-shadow-box",
                )}>
            {label}
        </button>
    );
}
