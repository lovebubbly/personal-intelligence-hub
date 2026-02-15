import { EventItem } from "@/types";

interface EventCalendarProps {
  events: EventItem[];
}

const kindLabel: Record<EventItem["kind"], string> = {
  token_unlock: "Token Unlock",
  model_release: "Model Release",
  conference: "Conference",
  governance: "Governance"
};

const domainBadge: Record<EventItem["domain_id"], string> = {
  crypto: "🪙",
  ai_ml: "🤖"
};

export function EventCalendar({ events }: EventCalendarProps) {
  if (!events.length) {
    return (
      <div className="rounded-2xl border border-border bg-card p-5 text-sm text-muted" data-testid="event-calendar-empty">
        예정된 이벤트가 없습니다.
      </div>
    );
  }

  return (
    <div className="space-y-2" data-testid="event-calendar">
      {events
        .slice()
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
        .map((event) => (
          <article key={event.id} className="rounded-xl border border-border bg-card/75 p-3">
            <div className="flex items-center justify-between gap-2 text-xs text-muted">
              <span>
                {domainBadge[event.domain_id]} {kindLabel[event.kind]}
              </span>
              <time dateTime={event.date}>{new Date(event.date).toLocaleString("ko-KR", { hour12: false })}</time>
            </div>
            <p className="mt-1 text-sm text-foreground/90">{event.title}</p>
          </article>
        ))}
    </div>
  );
}
