import { createContext } from "react";

export interface ContextProps {
    pets: number;
    setPets: (value: number) => void;
    totalPets: number;
    setTotalPets: (value: number) => void;
    petsPerSecond: number;
    setPetsPerSecond: (value: number) => void;
}

export const Context = createContext({} as ContextProps);