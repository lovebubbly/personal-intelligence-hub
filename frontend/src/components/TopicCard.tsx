import Link from "next/link";

import { DomainSlug, TopicStat } from "@/types";

interface TopicCardProps {
  domain: DomainSlug;
  stat: TopicStat;
}

export function TopicCard({ domain, stat }: TopicCardProps) {
  const sentimentTone = stat.sentiment_avg >= 20 ? "text-emerald-300" : stat.sentiment_avg <= -20 ? "text-rose-300" : "text-amber-200";

  return (
    <article className="rounded-2xl border border-border bg-card/85 p-4" data-testid="topic-card">
      <div className="flex items-center justify-between gap-2">
        <h3 className="text-base font-semibold text-foreground">{stat.topic}</h3>
        <span className={`text-xs ${sentimentTone}`}>sentiment {stat.sentiment_avg}</span>
      </div>
      <p className="mt-2 text-xs text-muted">24h signal {stat.signal_count_24h}</p>
      {stat.top_items[0] ? (
        <p className="mt-2 line-clamp-2 text-sm text-foreground/85">{stat.top_items[0].content}</p>
      ) : (
        <p className="mt-2 text-sm text-muted">상위 이벤트가 없습니다.</p>
      )}
      <Link
        href={`/topic/${domain}/${encodeURIComponent(stat.topic.toLowerCase())}`}
        className="mt-3 inline-flex text-xs text-accent underline-offset-2 hover:underline"
      >
        토픽 상세 보기
      </Link>
    </article>
  );
}
