import { Context } from "@/app/context";
import clsx from "clsx";
import { useContext } from "react";

interface UpgradesItemsProps {
    name: string
    image: string,
    cost: number,
}

export function UpgradesItem({ name, image, cost }: UpgradesItemsProps) {
    const { pets, setPets } = useContext(Context);
    return (
        <div className={clsx(
            "inline-flex", "flex-col", "items-center", "justify-around",
            "p-2", "overflow-hidden",
            "bg-orange-600", "drop-shadow-box",
            pets >= cost ? "grayscale-0 hover:bg-orange-700" : "grayscale-100",
            "transition-all", "duration-150",
        )} onClick={() => {
            if (cost > pets) return;
            setPets(pets - cost)
        }}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={image} alt={name} className={clsx("max-w-8/10", "h-auto", "max-h-8/10", "rounded-xl")}/>
            <p className={clsx("font-normal", "text-black", "text-nowrap", "text-clip")}>
                {name}
            </p>
        </div>
    );
}