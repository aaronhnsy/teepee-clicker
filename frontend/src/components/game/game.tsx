"use client";

import { Context } from "@/app/context";
import { ClickerPanel } from "@/layout/clicker";
import { UpgradesPanel } from "@/layout/upgrades";
import clsx from "clsx";
import { useEffect, useState } from "react";

export function Game() {
    const [pets, setPets] = useState(0);
    const [petsPerSecond, setPetsPerSecond] = useState(0);
    const [clickPower, setClickPower] = useState(1);

    useEffect(() => {
        const id = setInterval(() => {
            setPets(pets + petsPerSecond);
        }, 1000);
        return () => clearInterval(id);
    });

    return (
        <div className={clsx(
            "flex", "flex-col-reverse", "md:flex-row",
            "gap-2", "w-full", "h-full", "overflow-hidden",
        )}>
            <Context value={{
                pets, setPets,
                petsPerSecond, setPetsPerSecond,
                clickPower, setClickPower,
            }}>
                <ClickerPanel/>
                <UpgradesPanel/>
            </Context>
        </div>
    );
}