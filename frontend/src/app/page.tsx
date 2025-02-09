import { getCurrentUser } from "@/actions/common";
import { GameContainer } from "@/components/game";
import { LoginForm } from "@/layout/auth";
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
                <LoginForm/>
            </div>
        );
    }
    return <GameContainer/>;
}