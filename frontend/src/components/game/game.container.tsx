import { getCurrentUser } from "@/actions/common";
import { Game } from "./game";

export async function GameContainer() {
    const user = await getCurrentUser();
    if (user === null) {
        throw new Error("User not found");
    }
    return (
        <Game initial={Number(user.pets)}/>
    );
}