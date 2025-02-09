import { createContext } from "react";

export interface ContextProps {
    pets: number;
    setPets: (value: number) => void;
    petsPerSecond: number;
    setPetsPerSecond: (value: number) => void;
    clickPower: number;
    setClickPower: (value: number) => void;
}

export const Context = createContext({} as ContextProps);