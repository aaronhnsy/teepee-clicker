import { createContext, type Dispatch, type SetStateAction } from "react";

export interface ContextProps {
    pets: number;
    setPets: Dispatch<SetStateAction<number>>;
    petsPerClick: number;
    setPetsPerClick: Dispatch<SetStateAction<number>>;
    petsPerSecond: number;
    setPetsPerSecond: Dispatch<SetStateAction<number>>;

}

export const Context = createContext({} as ContextProps);