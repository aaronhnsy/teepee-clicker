import type { ChildrenProps } from "@/app/types";
import { Be_Vietnam_Pro } from "next/font/google"; // eslint-disable-line camelcase
import "@/styles/global.css";

const font = Be_Vietnam_Pro({
    subsets: ["latin", "latin-ext"],
    weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
});

export default function Layout({ children }: ChildrenProps) {
    return (
        <html suppressHydrationWarning lang="en" className={font.className}>
        <body>
        {children}
        </body>
        </html>
    );
}