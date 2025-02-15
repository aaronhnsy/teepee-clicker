import clsx from "clsx";
import { UpgradesItem } from "./upgrades.item";

export function UpgradesPanel() {
    return (
        <div className={clsx(
            "grid", "grid-cols-1",
            "gap-2", "p-2", "w-full", "h-2/3", "md:w-2/3", "md:h-full", "overflow-scroll",
            "bg-orange-500", "drop-shadow-box",
        )}>
            <UpgradesItem name="auto petter" image="/upgrades/01_auto_petter.gif"
                          cost={50} clickPowerIncrease={0} petsPerSecondIncrease={2}/>
            <UpgradesItem name="tipi" image="/upgrades/02_tipi.png"
                          cost={150} clickPowerIncrease={0} petsPerSecondIncrease={10}/>
            <UpgradesItem name="sleepy" image="/upgrades/03_sleepy.png"
                          cost={400} clickPowerIncrease={0} petsPerSecondIncrease={20}/>
            <UpgradesItem name="opps" image="/upgrades/04_opps.png"
                          cost={1000} clickPowerIncrease={2} petsPerSecondIncrease={0}/>
            <UpgradesItem name="hunger" image="/upgrades/05_hunger.png"
                          cost={3000} clickPowerIncrease={4} petsPerSecondIncrease={0}/>
            <UpgradesItem name="scream" image="/upgrades/06_scream.png"
                          cost={9000} clickPowerIncrease={6} petsPerSecondIncrease={10}/>
            <UpgradesItem name="bnuuy" image="/upgrades/07_bnuuy.png"
                          cost={20000} clickPowerIncrease={10} petsPerSecondIncrease={20}/>
            <UpgradesItem name="stretchies" image="/upgrades/08_stretchies.png"
                          cost={30000} clickPowerIncrease={10} petsPerSecondIncrease={20}/>
            <UpgradesItem name="mlem" image="/upgrades/09_mlem.png"
                          cost={50000} clickPowerIncrease={10} petsPerSecondIncrease={20}/>
        </div>
    );
}