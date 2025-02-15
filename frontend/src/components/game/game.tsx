"use client";

import { Context } from "@/app/context";
import { ClickerPanel } from "@/layout/clicker";
import { UpgradesPanel } from "@/layout/upgrades";
import clsx from "clsx";
import { useEffect, useState } from "react";

export function Game({ initial }: { initial: number }) {
    const [pets, setPets] = useState(initial);
    const [petsPerClick, setPetsPerClick] = useState(1);
    const [petsPerSecond, setPetsPerSecond] = useState(0);

    useEffect(() => {
        const id = setInterval(() => {
            setPets((p) => p + petsPerSecond);
        }, 1000);
        return () => clearInterval(id);
    }, [petsPerSecond]);

    return (
        <div className={clsx(
            "flex", "flex-col-reverse", "md:flex-row",
            "gap-2", "w-full", "h-full", "overflow-hidden",
        )}>
            <Context value={{
                pets, setPets,
                petsPerClick, setPetsPerClick,
                petsPerSecond, setPetsPerSecond,
            }}>
                <ClickerPanel/>
                <UpgradesPanel/>
            </Context>
        </div>
    );
}