import { DigestResponse, DomainInfo, DomainSlug, EventItem, FeedItem, Kol, TopicStat } from "@/types";

const now = new Date();
const iso = now.toISOString();
const earlier = new Date(now.getTime() - 18 * 60 * 1000).toISOString();
const muchEarlier = new Date(now.getTime() - 56 * 60 * 1000).toISOString();

export const mockDomains: DomainInfo[] = [
  {
    id: "crypto",
    display_name: "🪙 Crypto",
    is_active: true,
    topics: ["BTC", "ETH", "SOL", "SUI"],
    action_signals: {
      opportunity: { icon: "🟢", description: "매수/참여 기회" },
      watch: { icon: "🟡", description: "주시 필요" },
      risk: { icon: "🔴", description: "리스크 경고" },
      neutral: { icon: "⚪", description: "정보성" }
    }
  },
  {
    id: "ai_ml",
    display_name: "🤖 AI/ML",
    is_active: true,
    topics: ["LLM", "Agent", "Vision", "Safety", "Infra"],
    action_signals: {
      apply: { icon: "🟢", description: "바로 적용 가능" },
      learn: { icon: "🟡", description: "학습 필요" },
      paradigm_shift: { icon: "🔴", description: "전략 재검토" },
      neutral: { icon: "⚪", description: "정보성" }
    }
  }
];

export const mockFeed: FeedItem[] = [
  {
    id: "demo-1",
    domain_id: "crypto",
    source_type: "twitter",
    author: "@zachxbt",
    content: "SOL ecosystem exploit report confirmed. Patch rollout in progress.",
    url: "https://x.com/i/web/status/123456789",
    collected_at: iso,
    is_signal: true,
    importance_score: 9,
    sentiment_score: -72,
    action_signal: "risk",
    context_summary: "SOL 생태계 보안 이슈로 단기 변동성 확대 가능성이 높습니다.",
    related_topics: ["SOL"],
    category: "hack"
  },
  {
    id: "demo-2",
    domain_id: "ai_ml",
    source_type: "github",
    author: "vllm-project",
    content: "vLLM release adds production-ready speculative decoding path for agent loops.",
    url: "https://github.com/vllm-project/vllm/releases",
    collected_at: earlier,
    is_signal: true,
    importance_score: 8,
    sentiment_score: 61,
    action_signal: "apply",
    context_summary: "에이전트 워크로드에서 처리량 개선이 가능해 즉시 적용 가치가 큽니다.",
    related_topics: ["LLM", "Agent", "Infra"],
    category: "open_source"
  },
  {
    id: "demo-3",
    domain_id: "crypto",
    source_type: "news",
    author: "CoinDesk",
    content: "BTC ETF inflow hits monthly high amid macro easing expectations.",
    url: "https://www.coindesk.com/",
    collected_at: muchEarlier,
    is_signal: true,
    importance_score: 8,
    sentiment_score: 64,
    action_signal: "opportunity",
    context_summary: "ETF 유입 확대가 BTC 수급 개선 신호로 해석됩니다.",
    related_topics: ["BTC"],
    category: "macro"
  }
];

export const mockDigests: Record<DomainSlug, DigestResponse> = {
  crypto: {
    domain_id: "crypto",
    digest_date: iso.slice(0, 10),
    topics: [
      {
        topic: "BTC",
        summary: "BTC는 ETF 자금 유입 확대와 함께 단기 강세 흐름을 유지했습니다.",
        detailed_analysis:
          "거시 완화 기대와 현물 수급 개선이 동반되었습니다. 단기 저항대 재시험 가능성이 높습니다. 과열 구간 접근 시 변동성 관리가 필요합니다.",
        sentiment_avg: 52,
        signal_count: 7,
        top_events: [
          {
            content: "ETF inflow rise",
            url: "https://www.coindesk.com/",
            action_signal: "opportunity"
          }
        ]
      }
    ]
  },
  ai_ml: {
    domain_id: "ai_ml",
    digest_date: iso.slice(0, 10),
    topics: [
      {
        topic: "Agent",
        summary: "Agent 프레임워크는 추론 비용 절감 중심으로 빠르게 재편되고 있습니다.",
        detailed_analysis:
          "모델 성능 경쟁보다 orchestration 품질이 중요해졌습니다. 도구 호출 안정성과 관측성이 핵심 병목으로 부상했습니다. vLLM 계열 최적화가 실무 채택을 가속화하고 있습니다.",
        sentiment_avg: 46,
        signal_count: 6,
        top_events: [
          {
            content: "vLLM speculative decoding updates",
            url: "https://github.com/vllm-project/vllm/releases",
            action_signal: "apply"
          }
        ]
      }
    ]
  }
};

export const mockKols: Kol[] = [
  {
    domain_id: "crypto",
    twitter_username: "zachxbt",
    display_name: "zachxbt",
    credibility_score: 0.95,
    follower_count: 900000,
    is_active: true
  },
  {
    domain_id: "crypto",
    twitter_username: "WuBlockchain",
    display_name: "Wu Blockchain",
    credibility_score: 0.9,
    follower_count: 1200000,
    is_active: true
  },
  {
    domain_id: "crypto",
    twitter_username: "Pentosh1",
    display_name: "Pentoshi",
    credibility_score: 0.91,
    follower_count: 780000,
    is_active: true
  },
  {
    domain_id: "ai_ml",
    twitter_username: "TestingCatalog",
    display_name: "TestingCatalog",
    credibility_score: 0.93,
    follower_count: 310000,
    is_active: true
  },
  {
    domain_id: "ai_ml",
    twitter_username: "_akhaliq",
    display_name: "akhaliq",
    credibility_score: 0.91,
    follower_count: 245000,
    is_active: true
  },
  {
    domain_id: "ai_ml",
    twitter_username: "OpenAI",
    display_name: "OpenAI",
    credibility_score: 0.96,
    follower_count: 4700000,
    is_active: true
  }
];

export const mockTopicStats: Record<DomainSlug, TopicStat[]> = {
  crypto: [
    {
      topic: "BTC",
      signal_count_24h: 7,
      sentiment_avg: 52,
      top_items: [
        {
          content: "BTC ETF inflow hits monthly high",
          url: "https://www.coindesk.com/",
          importance_score: 8,
          action_signal: "opportunity"
        }
      ]
    },
    {
      topic: "SOL",
      signal_count_24h: 5,
      sentiment_avg: -44,
      top_items: [
        {
          content: "SOL ecosystem exploit report confirmed",
          url: "https://x.com/i/web/status/123456789",
          importance_score: 9,
          action_signal: "risk"
        }
      ]
    }
  ],
  ai_ml: [
    {
      topic: "Agent",
      signal_count_24h: 6,
      sentiment_avg: 46,
      top_items: [
        {
          content: "vLLM release adds speculative decoding",
          url: "https://github.com/vllm-project/vllm/releases",
          importance_score: 8,
          action_signal: "apply"
        }
      ]
    },
    {
      topic: "LLM",
      signal_count_24h: 9,
      sentiment_avg: 58,
      top_items: [
        {
          content: "새 함수호출 스펙이 에이전트 정확도를 개선",
          url: "https://openai.com",
          importance_score: 8,
          action_signal: "learn"
        }
      ]
    }
  ]
};

export const mockEvents: EventItem[] = [
  {
    id: "evt-1",
    domain_id: "crypto",
    title: "SOL 보안 패치 후속 모니터링",
    date: iso,
    kind: "governance"
  },
  {
    id: "evt-2",
    domain_id: "crypto",
    title: "주요 토큰 언락 일정 점검",
    date: new Date(now.getTime() + 5 * 60 * 60 * 1000).toISOString(),
    kind: "token_unlock"
  },
  {
    id: "evt-3",
    domain_id: "ai_ml",
    title: "오픈소스 모델 릴리즈 브리핑",
    date: new Date(now.getTime() + 2 * 60 * 60 * 1000).toISOString(),
    kind: "model_release"
  },
  {
    id: "evt-4",
    domain_id: "ai_ml",
    title: "AgentOps 컨퍼런스 세션",
    date: new Date(now.getTime() + 24 * 60 * 60 * 1000).toISOString(),
    kind: "conference"
  }
];
