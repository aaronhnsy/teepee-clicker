import { cookies } from "next/headers";

export interface User {
    id: string,
    name: string,
    pets: string,
}

export async function request<T>(path: string): Promise<T | null> {
    const response = await fetch(
        `https://aarons-macbook-pro.panda-char.ts.net/api${path}`, {
            method: "GET",
            headers: { Cookie: (await cookies()).toString() },
        },
    );
    return response.ok ? await response.json() : null;
}

export async function getCurrentUser(): Promise<User | null> {
    return await request<User>(
        "/users/me",
    );
}
