import { Kol } from "@/types";

interface KolHeatmapProps {
  kols: Kol[];
}

const domainBadge: Record<Kol["domain_id"], string> = {
  crypto: "🪙 Crypto",
  ai_ml: "🤖 AI/ML"
};

export function KolHeatmap({ kols }: KolHeatmapProps) {
  if (!kols.length) {
    return (
      <div className="rounded-2xl border border-border bg-card p-5 text-sm text-muted" data-testid="kol-heatmap-empty">
        표시할 KOL 데이터가 없습니다.
      </div>
    );
  }

  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3" data-testid="kol-heatmap">
      {kols.map((kol) => (
        <div key={`${kol.domain_id}:${kol.twitter_username}`} className="rounded-2xl border border-border bg-card p-4">
          <div className="flex items-center justify-between gap-2">
            <div className="text-sm font-semibold">@{kol.twitter_username}</div>
            <span className="text-[11px] text-muted">{domainBadge[kol.domain_id]}</span>
          </div>
          <div className="mt-1 text-xs text-muted">credibility {Math.round(kol.credibility_score * 100)}%</div>
          <div className="mt-3 h-2 rounded-full bg-zinc-800">
            <div
              className="h-2 rounded-full bg-gradient-to-r from-amber-300 to-emerald-400"
              style={{ width: `${Math.round(kol.credibility_score * 100)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
