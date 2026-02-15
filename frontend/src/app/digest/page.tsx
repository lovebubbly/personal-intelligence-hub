import Link from "next/link";

import { DigestView } from "@/components/DigestView";
import { HeaderNav } from "@/components/HeaderNav";
import { fetchDigest } from "@/lib/api";
import { DomainSlug } from "@/types";

function resolveDomain(domain: string | undefined): DomainSlug {
  return domain === "ai_ml" ? "ai_ml" : "crypto";
}

export default async function DigestPage({
  searchParams
}: {
  searchParams: { domain?: string; date?: string };
}) {
  const domain = resolveDomain(searchParams.domain);
  const digest = await fetchDigest(domain, searchParams.date);

  return (
    <>
      <HeaderNav />
      <section className="space-y-4">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">일일 다이제스트</h1>
            <p className="text-sm text-muted">오늘 반드시 확인해야 할 토픽별 요약</p>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Link
              className={`rounded-xl border px-3 py-2 ${domain === "crypto" ? "border-amber-300/70" : "border-border"}`}
              href="/digest?domain=crypto"
              data-testid="digest-domain-crypto"
            >
              🪙 Crypto
            </Link>
            <Link
              className={`rounded-xl border px-3 py-2 ${domain === "ai_ml" ? "border-amber-300/70" : "border-border"}`}
              href="/digest?domain=ai_ml"
              data-testid="digest-domain-ai_ml"
            >
              🤖 AI/ML
            </Link>
          </div>
        </div>
        <DigestView digest={digest} />
      </section>
    </>
  );
}
