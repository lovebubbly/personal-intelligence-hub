import Link from "next/link";

import { HeaderNav } from "@/components/HeaderNav";
import { KolHeatmap } from "@/components/KolHeatmap";
import { fetchKols } from "@/lib/api";
import { DomainId } from "@/types";

function resolveDomain(domain: string | undefined): DomainId {
  if (domain === "crypto" || domain === "ai_ml") {
    return domain;
  }
  return "all";
}

export default async function KolsPage({
  searchParams
}: {
  searchParams: { domain?: string };
}) {
  const domain = resolveDomain(searchParams.domain);
  const kols = await fetchKols(domain);

  return (
    <>
      <HeaderNav />
      <section className="space-y-4">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">KOL Heatmap</h1>
            <p className="text-sm text-muted">도메인 신뢰도 기반 모니터링 우선순위</p>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Link
              className={`rounded-xl border px-3 py-2 ${domain === "all" ? "border-amber-300/70" : "border-border"}`}
              href="/kols?domain=all"
              data-testid="kols-domain-all"
            >
              All
            </Link>
            <Link
              className={`rounded-xl border px-3 py-2 ${domain === "crypto" ? "border-amber-300/70" : "border-border"}`}
              href="/kols?domain=crypto"
              data-testid="kols-domain-crypto"
            >
              🪙 Crypto
            </Link>
            <Link
              className={`rounded-xl border px-3 py-2 ${domain === "ai_ml" ? "border-amber-300/70" : "border-border"}`}
              href="/kols?domain=ai_ml"
              data-testid="kols-domain-ai_ml"
            >
              🤖 AI/ML
            </Link>
          </div>
        </div>
        <KolHeatmap kols={kols} />
      </section>
    </>
  );
}
