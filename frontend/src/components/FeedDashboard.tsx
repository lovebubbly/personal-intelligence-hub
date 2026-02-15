"use client";

import { useEffect, useMemo, useState } from "react";

import { DomainTabs } from "@/components/DomainTabs";
import { FeedList } from "@/components/FeedList";
import { getFeedSocket } from "@/lib/socket";
import { DomainId, FeedItem } from "@/types";

interface FeedDashboardProps {
  initialItems: FeedItem[];
  initialDomain?: DomainId;
  domainOptions?: DomainId[];
  title?: string;
  subtitle?: string;
}

const motionPreset = {
  layout: { type: "spring", stiffness: 300, damping: 28 },
  insertDuration: 0.22
};

function normalize(items: FeedItem[]): FeedItem[] {
  return [...items].sort((a, b) => {
    const importanceDiff = (b.importance_score ?? 0) - (a.importance_score ?? 0);
    if (importanceDiff !== 0) return importanceDiff;
    return new Date(b.collected_at).getTime() - new Date(a.collected_at).getTime();
  });
}

export function FeedDashboard({
  initialItems,
  initialDomain = "all",
  domainOptions = ["all", "crypto", "ai_ml"],
  title = "Personal Intelligence Hub",
  subtitle = "신호 중심 실시간 멀티도메인 인텔리전스 피드"
}: FeedDashboardProps) {
  const [domain, setDomain] = useState<DomainId>(initialDomain);
  const [items, setItems] = useState<FeedItem[]>(normalize(initialItems));

  useEffect(() => {
    const socket = getFeedSocket();
    socket.emit("subscribe", { domains: ["all", "crypto", "ai_ml"] });

    const onFeedItem = (incoming: FeedItem) => {
      setItems((prev) => normalize([incoming, ...prev.filter((item) => item.id !== incoming.id)]));
    };

    socket.on("feed:item", onFeedItem);
    return () => {
      socket.off("feed:item", onFeedItem);
    };
  }, []);

  useEffect(() => {
    if (!domainOptions.includes(domain)) {
      setDomain(domainOptions[0] ?? "all");
    }
  }, [domain, domainOptions]);

  const filteredItems = useMemo(() => {
    if (domain === "all") {
      return items;
    }
    return items.filter((item) => item.domain_id === domain);
  }, [items, domain]);

  return (
    <section className="space-y-4" data-testid="feed-dashboard" data-motion-preset={JSON.stringify(motionPreset)}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">{title}</h1>
          <p className="text-sm text-muted">{subtitle}</p>
        </div>
        <DomainTabs value={domain} onChange={setDomain} options={domainOptions} />
      </div>

      <FeedList items={filteredItems} />
    </section>
  );
}
