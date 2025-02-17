import { getCurrentUser } from "@/actions/common";
import { Link } from "@/components/clickables";
import { GameContainer } from "@/components/game";
import clsx from "clsx";

export default async function Page() {
    const user = await getCurrentUser();
    if (user === null) {
        return (
            <div className={clsx(
                "flex", "items-center", "justify-center", "text-center",
                "w-full", "h-full", "overflow-hidden",
                "bg-orange-500", "drop-shadow-box",
            )}>
                <div className={clsx(
                    "flex", "flex-col",
                    "gap-2", "min-w-fit", "w-1/2",
                    "transition-all",
                )}>
                    <Link href="/login" text="Login"/>
                    <Link href="/signup" text="Signup"/>
                </div>
            </div>
        );
    }
    return <GameContainer/>;
}
