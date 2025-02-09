"use client";

import { Context } from "@/app/context";
import clsx from "clsx";
import { useContext } from "react";

export function ClickerButton() {
    const { pets, setPets, clickPower } = useContext(Context);
    return (
        <div className={clsx(
            "h-4/5", "md:w-9/10", "md:h-auto",
            "drop-shadow-star-normal", "hover:drop-shadow-star-hover", "active:drop-shadow-star-active",
            "active:translate-x-2", "active:translate-y-2",
            "transition-all", "duration-150",
        )}>
            <img src="/clicker/teepee.png" alt="teepee" className={clsx(
                "h-full",
                "[mask-image:url('/clicker/mask.png')]", "[mask-size:contain]",
                "animate-spin", "hover:cursor-pointer",
            )} onClick={() => setPets(pets + (clickPower))}/>
        </div>
    );
}