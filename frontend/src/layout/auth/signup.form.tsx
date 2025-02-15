"use client";

import { type FormState, signup } from "@/actions/auth";
import { FormSubmitButton, FormTextInput } from "@/components/forms";
import { clsx } from "clsx";
import { useActionState } from "react";

const initialState: FormState = {
    message: "",
};

export function SignupForm() {
    const [state, formAction] = useActionState(signup, initialState);
    return (
        <form action={formAction} className={clsx(
            "p-2", "w-[90%]", "sm:w-[70%]", "md:w-[60%]", "lg:w-[40%]", "xl:w-[25%]", "overflow-hidden",
            "bg-orange-600", "drop-shadow-box",
        )}>
            <div className={clsx(
                "flex", "flex-col", "items-stretch", "justify-stretch",
                "space-y-2",
            )}>
                <FormTextInput type="text" fieldName="username" label="Username"/>
                <FormTextInput type="password" fieldName="password" label="Password"/>
                <FormSubmitButton label="signup button" text="signup" pendingText="loading..."/>
                {state?.message
                    ? (
                        <p className={clsx("px-1", "line-clamp-2", "text-md", "font-bold")}>
                            {state.message}
                        </p>
                    ) : null
                }
            </div>
        </form>
    );
}
