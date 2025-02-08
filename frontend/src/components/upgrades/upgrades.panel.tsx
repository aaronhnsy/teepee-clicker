import { UpgradesItem } from "./upgrades.item";
import clsx from "clsx";

export function UpgradesPanel() {
    return (
        <div className={clsx(
            "grid", "grid-cols-3", "grid-rows-3",
            "gap-2", "p-2", "w-full", "h-2/3", "md:w-2/3", "md:h-full",
            "bg-lime-600", "drop-shadow-layout-box",
        )}>
            <UpgradesItem name="auto petter" image="/auto_petter.gif" cost={10}/>
            <UpgradesItem name="tipi" image="/tipi.png" cost={20}/>
            <UpgradesItem name="sleepy" image="/sleepy.png" cost={30}/>
            <UpgradesItem name="opps" image="/opps.png" cost={40}/>
            <UpgradesItem name="hunger" image="/hunger.png" cost={50}/>
            <UpgradesItem name="scream" image="/scream.png" cost={60}/>
            <UpgradesItem name="bnuuy" image="/bnuuy.png" cost={70}/>
            <UpgradesItem name="stretchies" image="/stretchies.png" cost={80}/>
            <UpgradesItem name="mlem" image="/mlem.png" cost={90}/>
        </div>
    );
}