import Link from "next/link";
import { notFound } from "next/navigation";

import { ActionBadge } from "@/components/ActionBadge";
import { HeaderNav } from "@/components/HeaderNav";
import { fetchFeed, fetchTopicStats } from "@/lib/api";
import { ActionSignal, DomainSlug } from "@/types";

export default async function TopicPage({ params }: { params: { domain: string; slug: string } }) {
  if (params.domain !== "crypto" && params.domain !== "ai_ml") {
    notFound();
  }
  const domain = params.domain as DomainSlug;
  const topicName = decodeURIComponent(params.slug).toUpperCase();

  const [topicStats, feed] = await Promise.all([fetchTopicStats(domain), fetchFeed(domain)]);
  const target = topicStats.find((stat) => stat.topic.toUpperCase() === topicName);
  if (!target) {
    notFound();
  }

  const relatedFeed = feed
    .filter((item) => (item.related_topics ?? []).some((topic) => topic.toUpperCase() === topicName))
    .slice(0, 12);

  return (
    <>
      <HeaderNav />
      <section className="space-y-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">{topicName} Intelligence</h1>
            <p className="text-sm text-muted">도메인: {domain === "crypto" ? "🪙 Crypto" : "🤖 AI/ML"}</p>
          </div>
          <Link
            href={`/domain/${domain}`}
            className="rounded-xl border border-border px-3 py-2 text-sm hover:border-amber-300/70"
          >
            도메인으로 돌아가기
          </Link>
        </div>

        <article className="rounded-2xl border border-border bg-card p-5">
          <div className="flex items-center justify-between text-sm">
            <span>24h signal {target.signal_count_24h}</span>
            <span className="text-amber-200">sentiment {target.sentiment_avg}</span>
          </div>

          <div className="mt-4 space-y-3">
            {target.top_items.map((item, index) => (
              <div key={`${topicName}-top-${index}`} className="rounded-xl border border-border/70 bg-black/10 p-3">
                <div className="mb-2 flex items-center justify-between">
                  <ActionBadge signal={(item.action_signal as ActionSignal) ?? "neutral"} />
                  <span className="text-xs text-muted">importance {item.importance_score}</span>
                </div>
                <p className="text-sm text-foreground/90">{item.content}</p>
              </div>
            ))}
          </div>
        </article>

        <section className="space-y-3">
          <h2 className="text-lg font-semibold">관련 피드</h2>
          {relatedFeed.length ? (
            <div className="space-y-2">
              {relatedFeed.map((item) => (
                <article key={item.id} className="rounded-xl border border-border bg-card/70 p-3">
                  <div className="mb-1 flex items-center justify-between text-xs text-muted">
                    <span>{item.author ?? "unknown"}</span>
                    <ActionBadge signal={item.action_signal} />
                  </div>
                  <p className="text-sm text-foreground/90">{item.content}</p>
                  {item.url ? (
                    <a className="mt-2 inline-flex text-xs text-accent underline-offset-2 hover:underline" href={item.url}>
                      원문 보기
                    </a>
                  ) : null}
                </article>
              ))}
            </div>
          ) : (
            <div className="rounded-2xl border border-border bg-card p-4 text-sm text-muted">관련 피드가 없습니다.</div>
          )}
        </section>
      </section>
    </>
  );
}
