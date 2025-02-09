import { getCurrentUser } from "@/actions/common";
import { LoginForm } from "@/components/auth";
import clsx from "clsx";
import { redirect } from "next/navigation";

export default async function Page() {
    const user = await getCurrentUser();
    if (user) redirect("/game");
    return (
        <div className={clsx(
            "flex", "items-center", "justify-center", "text-center",
            "w-full", "h-full", "overflow-hidden",
            "bg-orange-500", "drop-shadow-box",
        )}>
            <LoginForm/>
        </div>
    );
}