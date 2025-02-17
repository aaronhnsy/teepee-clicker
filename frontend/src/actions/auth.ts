"use server";

import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { z } from "zod";

const authenticationSchema = z.object({
    username: z.string()
        .min(1, { message: "Username should not be empty." })
        .max(64, { message: "Username should be 32 characters or less." }),
    password: z.string()
        .min(1, { message: "Password should not be empty." }),
});

export interface FormState {
    message: string;
}

export async function login(previousState: FormState, formData: FormData): Promise<FormState> {
    // validate the form data
    const validationResult = authenticationSchema.safeParse({
        username: formData.get("username"),
        password: formData.get("password"),
    });
    if (!validationResult.success) {
        return { message: validationResult.error.errors[0].message };
    }
    // send the login request
    const response = await fetch(
        `${process.env.BASE}/api/sessions`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: validationResult.data.username,
                password: validationResult.data.password,
                description: "web login",
            }),
        },
    );
    if (!response.ok) {
        return { message: (await response.json()).reason };
    }
    (await cookies()).set({
        name: "__session_id",
        value: (await response.text()),
        maxAge: 60 * 60 * 24 * 31,
        expires: 60 * 60 * 24 * 31,
        secure: true,
        httpOnly: true,
        sameSite: "strict",
        path: "/",
    });
    redirect("/");
}

export async function logout(): Promise<void> {
    // TODO: DELETE @ /api/sessions
    (await cookies()).delete("__session_id");
    revalidatePath("/");
}

export async function signup(previousState: FormState, formData: FormData): Promise<FormState> {
    // validate the form data
    const validationResult = authenticationSchema.safeParse({
        username: formData.get("username"),
        password: formData.get("password"),
    });
    if (!validationResult.success) {
        return { message: validationResult.error.errors[0].message };
    }
    // send the login request
    const response = await fetch(
        `${process.env.BASE}/api/users`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: validationResult.data.username,
                password: validationResult.data.password,
            }),
        },
    );
    if (!response.ok) {
        return { message: (await response.json()).reason };
    }
    return await login(previousState, formData);
}
