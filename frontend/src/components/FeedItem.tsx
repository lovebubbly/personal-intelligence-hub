import { motion, useReducedMotion } from "framer-motion";

import { ActionBadge } from "@/components/ActionBadge";
import { FeedItem as FeedItemType } from "@/types";

interface FeedItemProps {
  item: FeedItemType;
}

const domainLabel: Record<FeedItemType["domain_id"], string> = {
  crypto: "🪙 Crypto",
  ai_ml: "🤖 AI/ML"
};

export function FeedItem({ item }: FeedItemProps) {
  const reduceMotion = useReducedMotion();
  const sentiment = item.sentiment_score ?? 0;
  const sentimentWidth = Math.max(0, Math.min(100, (sentiment + 100) / 2));

  return (
    <motion.article
      layout
      initial={reduceMotion ? false : { opacity: 0, y: 8 }}
      animate={reduceMotion ? { opacity: 1 } : { opacity: 1, y: 0 }}
      exit={reduceMotion ? { opacity: 0 } : { opacity: 0, y: -6 }}
      transition={reduceMotion ? { duration: 0.08 } : { duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
      className="rounded-2xl border border-border bg-card/90 p-4 shadow-[0_12px_30px_rgba(0,0,0,0.24)]"
      data-testid="feed-item"
      data-domain={item.domain_id}
    >
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2 text-xs text-muted">
          <span className="rounded-lg border border-border/70 bg-black/20 px-2 py-0.5 text-[11px] text-amber-200">
            {domainLabel[item.domain_id]}
          </span>
          <span>{item.author ?? "unknown"}</span>
        </div>
        <ActionBadge signal={item.action_signal} />
      </div>

      <p className="text-sm leading-6 text-foreground/95">{item.content}</p>
      <p className="mt-2 text-sm text-amber-200/90">{item.context_summary}</p>

      <div className="mt-3 flex items-center justify-between text-xs text-muted">
        <span>{item.related_topics?.join(", ") ?? "NO TOPIC"}</span>
        <span>importance {item.importance_score ?? 0}/10</span>
      </div>

      <div className="mt-2 h-2 overflow-hidden rounded-full bg-zinc-800">
        <div
          className="h-full rounded-full bg-gradient-to-r from-rose-400 via-amber-300 to-emerald-400"
          style={{ width: `${sentimentWidth}%` }}
        />
      </div>

      {item.url ? (
        <a
          className="mt-3 inline-flex text-xs text-accent underline-offset-2 hover:underline"
          href={item.url}
          target="_blank"
          rel="noreferrer"
        >
          원문 보기
        </a>
      ) : null}
    </motion.article>
  );
}
