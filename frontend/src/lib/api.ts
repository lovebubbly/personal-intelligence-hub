import {
  DigestResponse,
  DomainInfo,
  DomainSlug,
  EventItem,
  FeedItem,
  Kol,
  TopicStat
} from "@/types";
import { mockDigests, mockDomains, mockEvents, mockFeed, mockKols, mockTopicStats } from "@/lib/mock";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === "true";

async function safeFetch<T>(path: string, fallback: T): Promise<T> {
  if (USE_MOCK) {
    return fallback;
  }

  try {
    const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function fetchDomains(): Promise<DomainInfo[]> {
  return safeFetch("/domains", mockDomains);
}

export async function fetchFeed(domain: "all" | DomainSlug = "all"): Promise<FeedItem[]> {
  const fallback = domain === "all" ? mockFeed : mockFeed.filter((item) => item.domain_id === domain);
  return safeFetch(`/feed?domain=${domain}&limit=50&min_importance=1`, fallback);
}

export async function fetchDigest(domain: DomainSlug = "crypto", digestDate?: string): Promise<DigestResponse> {
  const targetDate = digestDate ?? new Date().toISOString().slice(0, 10);
  return safeFetch(`/digest?domain=${domain}&digest_date=${targetDate}`, mockDigests[domain]);
}

export async function fetchKols(domain: "all" | DomainSlug = "all"): Promise<Kol[]> {
  const fallback = domain === "all" ? mockKols : mockKols.filter((kol) => kol.domain_id === domain);
  return safeFetch(`/kols?domain=${domain}`, fallback);
}

export async function fetchTopicStats(domain: DomainSlug): Promise<TopicStat[]> {
  return safeFetch(`/topics/${domain}`, mockTopicStats[domain]);
}

export async function fetchEvents(domain: "all" | DomainSlug = "all"): Promise<EventItem[]> {
  const fallback = domain === "all" ? mockEvents : mockEvents.filter((event) => event.domain_id === domain);
  return safeFetch(`/events?domain=${domain}&limit=20`, fallback);
}
