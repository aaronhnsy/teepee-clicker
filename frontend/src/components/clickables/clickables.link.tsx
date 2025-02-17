import clsx from "clsx";
import NextLink from "next/link";

interface LinkProps {
    href: string;
    text: string;
}

export function Link({ href, text }: LinkProps) {
    return (
        <NextLink href={href} className={clsx(
            "inline-flex", "items-center", "justify-center", "text-center",
            "p-2",
            "text-black", "text-base", "font-medium",
            "bg-orange-600", "hover:bg-orange-700", "active:bg-orange-700", "focus:bg-orange-700",
            "hover:translate-0.25", "active:translate-0.25", "focus:translate-0.25",
            "transition-all", "drop-shadow-box",
        )}>
            {text}
        </NextLink>
    );
}
