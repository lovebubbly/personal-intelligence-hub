import clsx from "clsx";

import { ActionSignal } from "@/types";

const styles: Record<ActionSignal, string> = {
  opportunity: "bg-emerald-400/20 text-emerald-300 border-emerald-300/40",
  apply: "bg-emerald-400/20 text-emerald-300 border-emerald-300/40",
  watch: "bg-amber-400/20 text-amber-300 border-amber-300/40",
  learn: "bg-amber-400/20 text-amber-300 border-amber-300/40",
  risk: "bg-rose-400/20 text-rose-300 border-rose-300/40",
  paradigm_shift: "bg-rose-400/20 text-rose-300 border-rose-300/40",
  neutral: "bg-zinc-400/20 text-zinc-300 border-zinc-300/40"
};

const labels: Record<ActionSignal, string> = {
  opportunity: "🟢 OPPORTUNITY",
  apply: "🟢 APPLY",
  watch: "🟡 WATCH",
  learn: "🟡 LEARN",
  risk: "🔴 RISK",
  paradigm_shift: "🔴 PARADIGM",
  neutral: "⚪ NEUTRAL"
};

export function ActionBadge({ signal }: { signal: ActionSignal }) {
  const normalized = signal in styles ? signal : "neutral";
  return (
    <span className={clsx("rounded-xl border px-2.5 py-1 text-xs font-medium", styles[normalized])}>
      {labels[normalized]}
    </span>
  );
}
