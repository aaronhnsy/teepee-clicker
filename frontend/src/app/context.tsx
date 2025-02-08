import { createContext } from "react";

export interface ContextProps {
    pets: number;
    setPets: (value: number) => void;
}

export const Context = createContext({} as ContextProps);