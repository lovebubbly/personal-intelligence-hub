import { EventCalendar } from "@/components/EventCalendar";
import { FeedDashboard } from "@/components/FeedDashboard";
import { HeaderNav } from "@/components/HeaderNav";
import { TopicCard } from "@/components/TopicCard";
import { fetchEvents, fetchFeed, fetchTopicStats } from "@/lib/api";

export default async function HomePage() {
  const [feed, cryptoTopics, aiTopics, events] = await Promise.all([
    fetchFeed("all"),
    fetchTopicStats("crypto"),
    fetchTopicStats("ai_ml"),
    fetchEvents("all")
  ]);

  return (
    <>
      <HeaderNav />
      <FeedDashboard initialItems={feed} />

      <section className="mt-8 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Topic Intelligence</h2>
            <span className="text-xs text-muted">최근 24시간 핵심 토픽</span>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            {cryptoTopics.slice(0, 2).map((stat) => (
              <TopicCard key={`crypto-${stat.topic}`} domain="crypto" stat={stat} />
            ))}
            {aiTopics.slice(0, 2).map((stat) => (
              <TopicCard key={`ai-${stat.topic}`} domain="ai_ml" stat={stat} />
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Event Calendar</h2>
            <span className="text-xs text-muted">도메인 통합 일정</span>
          </div>
          <EventCalendar events={events} />
        </div>
      </section>
    </>
  );
}
