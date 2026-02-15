"use client";

import clsx from "clsx";
import { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
}

const sizeMap = {
  sm: "h-9 px-3 rounded-xl text-sm",
  md: "h-11 px-4 rounded-2xl text-sm font-semibold",
  lg: "h-14 px-6 rounded-3xl text-base font-semibold"
};

const variantMap = {
  primary:
    "bg-gradient-to-br from-amber-400 to-yellow-500 text-zinc-950 shadow-[0_8px_26px_rgba(250,204,21,0.35)] hover:brightness-105",
  outline:
    "bg-card text-foreground border border-border hover:border-amber-300/70 hover:bg-zinc-900",
  ghost: "bg-transparent text-foreground hover:bg-zinc-800/70"
};

export function Button({
  className,
  variant = "primary",
  size = "md",
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={clsx(
        "inline-flex items-center justify-center gap-2 whitespace-nowrap transition-transform duration-150 active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-300 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-900 disabled:cursor-not-allowed disabled:opacity-60",
        sizeMap[size],
        variantMap[variant],
        className
      )}
      {...props}
    />
  );
}
