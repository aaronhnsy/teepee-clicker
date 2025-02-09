"use client";

import { logout } from "@/actions/auth";

export function LogoutButton() {
    return (
        <button onClick={logout}>
            logout
        </button>
    );
}
