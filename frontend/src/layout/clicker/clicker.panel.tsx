"use client";

import { Context } from "@/app/context";
import clsx from "clsx";
import { useContext } from "react";
import { ClickerButton } from "./clicker.button";

export function ClickerPanel() {
    const { pets, petsPerClick, petsPerSecond } = useContext(Context);
    return (
        <div className={clsx(
            "flex", "flex-col", "items-center", "justify-evenly",
            "p-2", "w-full", "h-1/3", "md:w-1/3", "md:h-full",
            "bg-orange-500", "drop-shadow-box",
        )}>
            <div className={clsx("text-center")}>
                <h1 className={clsx(
                    "font-bold", "text-3xl", "text-black",
                    "[text-shadow:0.15rem_0.15rem_0.15rem_darkgray]",
                )}>
                    {`${petsPerClick} pet${petsPerClick === 1 ? "" : "s"} per click`}
                </h1>
                <h1 className={clsx(
                    "font-bold", "text-3xl", "text-black",
                    "[text-shadow:0.15rem_0.15rem_0.15rem_darkgray]",
                )}>
                    {`${petsPerSecond} pet${petsPerSecond === 1 ? "" : "s"}/s`}
                </h1>
                <h1 className={clsx(
                    "font-bold", "text-3xl", "text-black",
                    "[text-shadow:0.15rem_0.15rem_0.15rem_darkgray]",
                )}>
                    {`${pets} pet${pets === 1 ? "" : "s"}`}
                </h1>
            </div>
            <ClickerButton/>
        </div>
    );
}