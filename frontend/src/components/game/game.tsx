"use client";

import { Context } from "@/app/context";
import { PetsPanel } from "@/components/pets";
import { UpgradesPanel } from "@/components/upgrades";
import clsx from "clsx";
import { useMemo, useState } from "react";

interface GameProps {
    initialPetCount: number;
}

export function Game({ initialPetCount }: GameProps) {

    const [pets, setPets] = useState(initialPetCount);
    const [totalPets, setTotalPets] = useState(0);
    const contextMemo = useMemo(() => ({
        pets, setPets,
        totalPets, setTotalPets,
    }), [pets, totalPets]);

    // const [websocket, setWebsocket] = useState(new WebSocket("wss://aarons-macbook-pro.panda-char.ts.net/websocket"));
    // websocket.onmessage = (event) => {
    //     const message = JSON.parse(event.data);
    //     setTotalPets(message.total_pets);
    // };
    //
    // setInterval(() => {
    //     websocket.send(JSON.stringify({ pets }));
    // }, 1000);

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