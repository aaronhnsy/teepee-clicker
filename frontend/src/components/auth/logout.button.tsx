"use client";

import { logout } from "@/actions/auth";
import clsx from "clsx";

export function LogoutButton() {
    return (
        <button onClick={logout} className={clsx(
            "inline-flex", "items-center", "justify-center",
            "px-2",
            "bg-orange-600", "hover:bg-orange-700", "drop-shadow-box",
            "transition-colors",
        )}>
            logout
        </button>
    );
}
