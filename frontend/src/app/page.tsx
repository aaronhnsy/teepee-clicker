import { getCurrentUser } from "@/actions/common";
import { GameContainer } from "@/components/game";
import clsx from "clsx";
import Link from "next/link";

export default async function Page() {
    const user = await getCurrentUser();
    if (user === null) {
        return (
            <div className={clsx(
                "flex", "items-center", "justify-center", "text-center",
                "w-full", "h-full", "overflow-hidden",
                "bg-orange-500", "drop-shadow-box",
            )}>
                <Link href="/login" className={clsx(
                    "inline-flex", "items-center", "justify-center",
                    "px-2",
                    "bg-orange-600", "drop-shadow-box",
                )}>
                    Login
                </Link>
                <Link href="/signup" className={clsx(
                    "inline-flex", "items-center", "justify-center",
                    "px-2",
                    "bg-orange-600", "drop-shadow-box",
                )}>
                    Sign Up
                </Link>
            </div>
        );
    }
    return <GameContainer/>;
}
