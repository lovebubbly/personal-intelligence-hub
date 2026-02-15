import { notFound } from "next/navigation";

import { EventCalendar } from "@/components/EventCalendar";
import { FeedDashboard } from "@/components/FeedDashboard";
import { HeaderNav } from "@/components/HeaderNav";
import { TopicCard } from "@/components/TopicCard";
import { fetchEvents, fetchFeed, fetchTopicStats } from "@/lib/api";
import { DomainSlug } from "@/types";

const DOMAIN_META: Record<DomainSlug, { title: string; subtitle: string }> = {
  crypto: {
    title: "🪙 Crypto Domain Feed",
    subtitle: "온체인/시장/규제 시그널 중심 모니터링"
  },
  ai_ml: {
    title: "🤖 AI/ML Domain Feed",
    subtitle: "모델/논문/오픈소스 실무 시그널 모니터링"
  }
};

export default async function DomainPage({ params }: { params: { slug: string } }) {
  if (params.slug !== "crypto" && params.slug !== "ai_ml") {
    notFound();
  }

  const domain = params.slug as DomainSlug;
  const [feed, topics, events] = await Promise.all([fetchFeed(domain), fetchTopicStats(domain), fetchEvents(domain)]);

  return (
    <>
      <HeaderNav />
      <FeedDashboard
        initialItems={feed}
        initialDomain={domain}
        domainOptions={[domain]}
        title={DOMAIN_META[domain].title}
        subtitle={DOMAIN_META[domain].subtitle}
      />

      <section className="mt-8 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Topic Intelligence</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {topics.slice(0, 6).map((stat) => (
              <TopicCard key={`${domain}-${stat.topic}`} domain={domain} stat={stat} />
            ))}
          </div>
        </div>
        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Events</h2>
          <EventCalendar events={events} />
        </div>
      </section>
    </>
  );
}
