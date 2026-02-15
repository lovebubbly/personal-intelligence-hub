import { ActionBadge } from "@/components/ActionBadge";
import { ActionSignal, DigestResponse } from "@/types";

export function DigestView({ digest }: { digest: DigestResponse }) {
  if (!digest.topics.length) {
    return (
      <div className="rounded-2xl border border-border bg-card p-5 text-sm text-muted" data-testid="digest-empty">
        오늘 생성된 다이제스트가 없습니다.
      </div>
    );
  }

  return (
    <div className="space-y-4" data-testid="digest-view">
      {digest.topics.map((topic) => (
        <article key={topic.topic} className="rounded-2xl border border-border bg-card p-5">
          <div className="mb-2 flex items-center justify-between text-xs text-muted">
            <span className="font-semibold text-amber-200">{topic.topic}</span>
            <span>signals {topic.signal_count ?? 0}</span>
          </div>
          <h3 className="text-base font-semibold text-foreground">{topic.summary}</h3>
          <p className="mt-2 text-sm text-foreground/80">{topic.detailed_analysis}</p>

          {(topic.top_events ?? []).length ? (
            <div className="mt-3 space-y-2 border-t border-border/70 pt-3">
              {topic.top_events.slice(0, 3).map((event, idx) => (
                <div key={`${topic.topic}-${idx}`} className="rounded-xl border border-border/70 bg-black/10 p-2">
                  <div className="mb-1 flex items-center justify-between">
                    <ActionBadge signal={(event.action_signal as ActionSignal) ?? "neutral"} />
                    {event.url ? (
                      <a className="text-xs text-accent underline-offset-2 hover:underline" href={event.url} target="_blank" rel="noreferrer">
                        source
                      </a>
                    ) : null}
                  </div>
                  <p className="text-xs text-foreground/90">{event.content}</p>
                </div>
              ))}
            </div>
          ) : null}
        </article>
      ))}
    </div>
  );
}
