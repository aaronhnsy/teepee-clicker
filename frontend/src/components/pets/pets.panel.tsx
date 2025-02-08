"use client";

import { Context } from "@/app/context";
import clsx from "clsx";
import { useContext } from "react";
import { PetsStar } from "./pets.star";

export function PetsPanel() {
    const { pets } = useContext(Context);
    return (
        <div className={clsx(
            "flex", "flex-col", "items-center", "justify-evenly",
            "p-2", "w-full", "h-1/3", "md:w-1/3", "md:h-full",
            "bg-lime-600", "drop-shadow-layout-box",
        )}>
            <h1 className={clsx("font-bold", "text-3xl", "text-black", "[text-shadow:0.25rem_0.25rem_0.25rem_gray]")}>
                {`${pets} pet${pets === 1 ? "" : "s"}`}
            </h1>
            <PetsStar/>
        </div>
    );
}