import { getCurrentUser } from "@/actions/common";
import clsx from "clsx";

export async function Header() {
    const user = await getCurrentUser();
    return (
        <header className={clsx(
            "shrink-0", "flex", "flex-row", "items-stretch", "justify-end",
            "w-full", "h-10", "overflow-hidden",
            "bg-orange-500", "drop-shadow-box",
        )}>
            <div className={clsx(
                "inline-flex", "items-center", "justify-center",
                "px-2",
                "bg-orange-600", "drop-shadow-box",
            )}>
                {(user === null) ? ("not logged in") : (user.name)}
            </div>
        </header>
    );
}