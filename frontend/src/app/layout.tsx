import type { ChildrenProps } from "@/app/types";
import { Header } from "@/layout/header";
import clsx from "clsx";
import { Be_Vietnam_Pro } from "next/font/google";  // eslint-disable-line camelcase
import "@/styles/global.css";

const font = Be_Vietnam_Pro({
    subsets: ["latin", "latin-ext"],
    weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
});

export default function Layout({ children }: ChildrenProps) {
    return (
        <html suppressHydrationWarning lang="en" className={font.className}>
        <body>
        <div className={clsx(
            "flex", "flex-col", "items-stretch", "justify-stretch",
            "gap-2", "p-2", "w-full", "h-dvh", "overflow-hidden",
            "bg-orange-400",
        )}>
            <Header/>
            {children}
        </div>
        </body>
        </html>
    );
}