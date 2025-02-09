"use client";

import { Context } from "@/app/context";
import { PetsPanel } from "@/components/pets";
import { UpgradesPanel } from "@/components/upgrades";
import clsx from "clsx";
import { useMemo, useState } from "react";

export default function Page() {
    const [pets, setPets] = useState(0);
    const contextMemo = useMemo(() => ({
        pets, setPets,
    }), [pets]);
    return (
        <div className={clsx(
            "flex", "flex-col-reverse", "md:flex-row",
            "gap-2", "w-full", "h-full", "overflow-hidden",
        )}>
            <Context value={contextMemo}>
                <PetsPanel/>
                <UpgradesPanel/>
            </Context>
        </div>
    );
}