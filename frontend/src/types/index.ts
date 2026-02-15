export type DomainSlug = "crypto" | "ai_ml";
export type DomainId = "all" | DomainSlug;

export type ActionSignal =
  | "opportunity"
  | "watch"
  | "risk"
  | "apply"
  | "learn"
  | "paradigm_shift"
  | "neutral";

export interface FeedItem {
  id: string;
  domain_id: DomainSlug;
  source_type: string;
  author: string | null;
  content: string;
  url: string | null;
  collected_at: string;
  is_signal: boolean;
  importance_score: number | null;
  sentiment_score: number | null;
  action_signal: ActionSignal;
  context_summary: string | null;
  related_topics: string[] | null;
  category: string | null;
}

export interface DomainInfo {
  id: DomainSlug;
  display_name: string;
  is_active: boolean;
  topics: string[];
  action_signals: Record<string, { icon: string; description: string }>;
}

export interface DigestTopic {
  topic: string;
  summary: string;
  detailed_analysis: string | null;
  sentiment_avg: number | null;
  signal_count: number | null;
  top_events: Array<{ content: string; url: string | null; action_signal: string }>;
}

export interface DigestResponse {
  domain_id: DomainSlug;
  digest_date: string;
  topics: DigestTopic[];
}

export interface Kol {
  domain_id: DomainSlug;
  twitter_username: string;
  display_name: string | null;
  credibility_score: number;
  follower_count: number | null;
  is_active: boolean;
}

export interface TopicStat {
  topic: string;
  signal_count_24h: number;
  sentiment_avg: number;
  top_items: Array<{
    content: string;
    url: string | null;
    importance_score: number;
    action_signal: string;
  }>;
}

export interface EventItem {
  id: string;
  domain_id: DomainSlug;
  title: string;
  date: string;
  kind: "token_unlock" | "model_release" | "conference" | "governance";
}
