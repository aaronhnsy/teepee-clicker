import { Context } from "@/app/context";
import clsx from "clsx";
import { useContext, useState } from "react";

interface UpgradesItemsProps {
    name: string
    image: string,
    cost: number,
    petsPerSecondIncrease: number;
    clickPowerIncrease: number;
}

export function UpgradesItem({ name, image, cost, petsPerSecondIncrease, clickPowerIncrease }: UpgradesItemsProps) {
    const { pets, setPets, petsPerSecond, setPetsPerSecond, petsPerClick, setPetsPerClick } = useContext(Context);
    const [count, setCount] = useState(0);
    return (
        <div className={clsx(
            "flex", "flex-row",
            "p-2", "min-h-20", "overflow-hidden",
            "bg-orange-600", "drop-shadow-box",
            pets >= cost ? "grayscale-0 hover:bg-orange-700" : "grayscale-100",
            "transition-all", "duration-150",
        )} onClick={() => {
            if (cost > pets) return;
            setPets(pets - cost);
            setCount(count + 1);
            setPetsPerSecond(petsPerSecond + petsPerSecondIncrease);
            setPetsPerClick(petsPerClick + clickPowerIncrease);
        }}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={image} alt={name} className={clsx("w-auto", "h-full", "rounded-xl")}/>
            <p className={clsx("grow", "justify-self-center", "place-self-center", "text-center", "font-normal", "text-black", "text-nowrap", "text-clip")}>
                {`$${cost} - ${name} (${count})`}
            </p>
        </div>
    );
}