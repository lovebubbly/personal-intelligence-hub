# Personal Intelligence Hub — AI 기반 멀티도메인 인텔리전스 대시보드

## 🎯 프로젝트 개요

**한줄 요약**: 크립토, AI/ML, 테크 등 **내가 중요시하는 도메인**의 KOL 트윗, 뉴스, 논문, GitHub 릴리즈, 온체인 시그널을 AI가 수집·필터링·분석하여 단일 대시보드로 제공하는 **개인 맞춤형 멀티도메인 인텔리전스 플랫폼**.

> X에서 하루종일 타임라인 새로고침할 필요 없이, AI가 **"지금 당장 알아야 할 것"**만 도메인별로 골라서 보여주는 나만의 인텔리전스 레이더 🧠
> 

### 🌐 지원 도메인 (v1)

| **도메인** | **핵심 소스** | **액션 시그널 의미** |
| --- | --- | --- |
| 🪙 **Crypto** | X KOL, 뉴스, 온체인, 규제 | 🟢 매수 기회 / 🟡 주시 / 🔴 리스크 |
| 🤖 **AI/ML** | X, arXiv, GitHub, 공식 블로그 | 🟢 바로 적용 가능 / 🟡 학습 필요 / 🔴 패러다임 전환 |
| 🔧 **Tech** (향후) | X, RSS, ProductHunt, HackerNews | 🟢 도입 추천 / 🟡 관망 / 🔴 보안 이슈 |
| 🎨 **Custom** (향후) | 사용자 정의 소스 | 사용자 정의 시그널 |

---

## 🔥 문제 정의 (Pain Point)

<aside>
⚠️

**핵심 문제**: 관심 도메인이 늘어날수록 모니터링 비용이 선형 증가하고, 중요한 시그널을 놓치기 쉽다. X 타임라인을 하루종일 새로고침하는 건 해결책이 아니다.

</aside>

- **소스 파편화**: X, Telegram, Discord, 뉴스, arXiv, GitHub, 온체인 데이터 등 도메인마다 수십 개 채널
- **노이즈 > 시그널**: 크립토는 99%가 실링, AI는 과장된 하이프 — 진짜 알파를 찾으려면 엄청난 시간 소모
- **KOL 트래킹 한계**: 크립토 KOL 100명 + AI 리서처 50명 + 테크 저널리스트 30명 = 타임라인 폭발
- **도메인 간 연결 부재**: 크립토 뉴스는 CoinDesk, AI 뉴스는 TestingCatalog, 논문은 arXiv... 각각 따로 체크해야 함
- **뉴스 사이트 지연**: 정제된 뉴스 사이트는 느림 — X에서 먼저 터지고, 공식 블로그/arXiv에서 디테일이 나옴

---

## 💡 솔루션 — 핵심 기능 & 차별화

<aside>
💎

**차별화 핵심**: 단순 "뉴스 모음"이 아니라 **도메인별 AI 필터링 + 맥락 분석 + 도메인 맞춤 액션 시그널** 제공. "뭐가 있었다"가 아니라 **"이게 왜 중요하고 어떻게 대응해야 하는지"**를 도메인 맥락에 맞게.

</aside>

### 📥 데이터 수집 레이어 (도메인 공통 파이프라인)

수집기는 **도메인에 독립적인 플러그인 구조** — 새 도메인 추가 시 소스 플러그인만 등록하면 됨.

- **KOL 트래커**: 도메인별 KOL 리스트 기반 X 트윗 실시간 수집 (X API v2)
- **뉴스 어그리게이터**: 도메인별 RSS 소스 30+ (크립토: CoinDesk, The Block / AI: OpenAI Blog, HuggingFace 등)
- **학술 수집기** (AI 도메인): arXiv [cs.AI](http://cs.AI), [cs.CL](http://cs.CL), cs.LG daily papers
- **코드 수집기** (AI 도메인): GitHub trending, 주요 오픈소스 릴리즈 모니터링
- **정책 모니터** (크립토 도메인): SEC, CFTC, 한국 금융위원회 규제 동향
- **온체인 알림** (크립토 도메인): 고래 지갑 이동, DEX 대량 거래 (Whale Alert, Dune)

### 🧠 AI 분석 레이어 (이것이 차별점)

- **도메인 맞춤 노이즈 필터**: 도메인별 전용 프롬프트로 "실링/하이프" vs "실제 알파" 분류 (정확도 90%+)
- **맥락 요약**: "왜 이게 중요한지" 도메인 맥락 기반 한 문장 자동 생성
- **센티먼트 스코어**: 토픽별 실시간 감성 지수
- **크로스도메인 연결 분석**: "AI 칩 수출 규제 발표 → 관련 크립토 AI 토큰 하락" 같은 도메인 간 인과 추론
- **도메인별 액션 시그널**: 크립토는 매수/리스크, AI는 학습/적용/패러다임 전환 등 맥락에 맞는 시그널

### 📊 대시보드 UI

- **통합 피드**: 전체 도메인 필터링된 타임라인 (중요도순) + 도메인별 탭 필터
- **도메인별 인텔리전스 카드**: 크립토는 코인별, AI는 토픽별(LLM/Vision/Agent 등) 종합 요약
- **KOL 히트맵**: 도메인별 누가 뭘 말하고 있는지 한눈에
- **이벤트 캘린더**: 크립토(토큰 언락, 에어드랍) + AI(컨퍼런스, 모델 출시) 통합 일정
- **쓰레드 생성**: 분석 결과를 X 쓰레드 형태로 자동 작성 (콘텐츠 크리에이터용)
- **개인 관심사 튜닝**: 도메인 내 세부 토픽 가중치 조절 (예: "LLM Agent" 높이고 "Computer Vision" 낮추기)

---

## 📊 경쟁 환경 분석

### 크립토 도메인 경쟁사

| **서비스** | **강점** | **약점** | **우리의 차별점** |
| --- | --- | --- | --- |
| CoinMarketCap | 종합 데이터, 브랜드 | 뉴스/소셜 분석 약함 | AI 맥락 분석 + KOL 트래킹 |
| Whale Alert | 온체인 특화 | 뉴스/소셜 없음 | 올인원 (온체인+소셜+뉴스) |
| Coindive | 소셜 미디어 트래킹 | AI 분석 깊이 부족 | LLM 기반 심층 맥락 분석 |
| Token Metrics | AI 예측, 포트폴리오 | 비쌆 ($50+/월) | 소셜 인텔리전스 특화 + 저가 |

### AI/테크 도메인 경쟁사

| **서비스** | **강점** | **약점** | **우리의 차별점** |
| --- | --- | --- | --- |
| Feedly + AI | RSS 통합, AI 요약, 대중적 | 도메인 특화 없음, 액션 시그널 없음 | 도메인별 맞춤 필터/시그널 + KOL 트래킹 |
| Papers With Code | 논문+코드 연결, 학술 특화 | 뉴스/소셜 없음, 액션 시그널 없음 | 논문 + 소셜 + 뉴스 통합 파이프라인 |
| TestingCatalog / @_akhaliq | 빠른 속보, 커뮤니티 활발 | X 의존, 필터링 없음, 노이즈 섬임 | AI가 노이즈 제거 + 맥락 분석 자동화 |
| [daily.dev](http://daily.dev) | 개발자 뉴스 커레이션 | AI/ML 도메인 심층 분석 부족 | 도메인 전문성 + 크로스도메인 연결 |

### 멀티도메인 통합 관점

<aside>
🎯

**핵심 포지션**: 기존 서비스들은 모두 **단일 도메인 특화**. 멀티도메인을 하나의 파이프라인으로 통합하고, 도메인 간 연결 분석까지 제공하는 서비스는 없음. 이게 우리의 **블루오션**.

</aside>

---

## 🏗️ 기술 스택

| 영역 | 기술 | 멀티도메인 고려사항 |
| --- | --- | --- |
| 데이터 수집 | X API v2 + RSS 파서 + Whale Alert API + Dune API + arXiv API + GitHub API | 도메인별 수집기 플러그인 구조 |
| AI 필터/분석 | Gemini Flash (필터링) + Claude Sonnet (심층 분석) | 도메인별 전용 프롬프트 템플릿 |
| 실시간 처리 | Redis Streams (Kafka 대신 경량) | 도메인별 채널 분리 |
| 프론트엔드 | Next.js 14 + TailwindCSS + [Socket.io](http://Socket.io) (실시간) | 도메인 탭 필터 + 통합 피드 UI |
| 백엔드 | Python 3.12 + FastAPI + APScheduler + PostgreSQL | 도메인 레지스트리 패턴 |
| DB | Supabase (PostgreSQL) | `domain` 필드 기반 테이블 설계 |
| 알림 | Telegram Bot API | 도메인별 구독/필터 설정 |
| 배포 | Vercel (FE) + Railway (BE + Redis) | — |

---

## 🎯 MVP 범위 (5-6주)

### Phase 1: 코어 파이프라인 + 크립토 도메인 (Week 1-3)

- [ ]  도메인 추상화 레이어 설계 (domain registry, 수집기 플러그인 인터페이스)
- [ ]  DB 스키마 마이그레이션 (`domain` 필드 포함)
- [ ]  크립토 KOL 20명 트윗 자동 수집 (X API)
- [ ]  크립토 뉴스 RSS 수집기
- [ ]  도메인별 노이즈 필터 파이프라인 (Gemini Flash)
- [ ]  심층 분석 + 액션 시그널 분류 (Claude Sonnet)
- [ ]  크립토 일일 다이제스트 자동 생성
- [ ]  Telegram 봇 기본 기능 (구독, 도메인 필터, 알림)

### Phase 2: AI/ML 도메인 추가 (Week 3-5)

- [ ]  AI/ML KOL 15명 트윗 수집 추가
- [ ]  AI 도메인 전용 RSS 소스 (OpenAI Blog, HuggingFace, Anthropic 등)
- [ ]  arXiv daily papers 수집기 ([cs.AI](http://cs.AI), [cs.CL](http://cs.CL), cs.LG)
- [ ]  GitHub trending 수집기 (Python/ML 태그)
- [ ]  AI 도메인 전용 노이즈 필터 프롬프트
- [ ]  AI 도메인 액션 시그널 체계 (학습/적용/패러다임 전환)
- [ ]  AI 도메인 일일 다이제스트

### Phase 3: 통합 대시보드 UI (Week 4-6)

- [ ]  통합 피드 대시보드 (도메인 탭 필터 + 중요도순)
- [ ]  도메인별 인텔리전스 카드 (코인별 / AI 토픽별)
- [ ]  KOL 히트맵 (도메인 통합)
- [ ]  통합 이벤트 캘린더
- [ ]  크로스도메인 연결 분석 기본
- [ ]  통합 테스트 + 배포

---

## 💰 수익 모델

| 모델 | 내용 | 가격 |
| --- | --- | --- |
| Free | 도메인 1개, 일일 AI 요약 1회, 기본 피드 | 무료 |
| Alpha | 도메인 3개, 실시간 피드, KOL 트래킹, 센티먼트 | $9.99/월 |
| Pro | 무제한 도메인, 커스텀 도메인 생성, 쓰레드 생성, 크로스도메인 분석, API | $24.99/월 |

---

## ⚠️ 리스크 & 과제

| 리스크 | 심각도 | 대응 |
| --- | --- | --- |
| X API 비용 & 제한 | 🔴 높음 | 효율적 폴링 + 캐싱, 도메인 간 KOL 수집 통합 |
| "뉴스 모음" 이상의 가치 증명 | 🔴 높음 | **AI 분석 품질**이 생명 — 도메인별 프롬프트 튜닝 지속 |
| 도메인 확장 시 복잡도 증가 | 🔴 높음 | 도메인 추상화 레이어로 플러그인 구조 유지 |
| KOL 발언의 신뢰도 문제 | 🟡 중간 | KOL 신뢰도 스코어링 시스템 구축 |
| 법적 이슈 (콘텐츠 재가공) | 🟡 중간 | 요약/분석은 fair use, 원문 링크 제공 |
| arXiv/GitHub API rate limit | 🟡 중간 | daily batch 수집 (실시간 불필요), 캐싱 적극 활용 |

---

## 🤖 에이전틱 코딩 프롬프트

<aside>
⚡

아래 프롬프트를 **Claude Code / Cursor Agent / Cline** 등 에이전틱 코딩 도구에 붙여넣으면 MVP를 구축할 수 있습니다.

</aside>

```
# 프로젝트: Personal Intelligence Hub — AI 기반 멀티도메인 인텔리전스 대시보드 (MVP)

## 1. 프로젝트 개요
크립토, AI/ML 등 사용자가 관심있는 도메인의 KOL 트윗, 뉴스, 논문, GitHub 릴리즈, 온체인 시그널을 AI가 수집·필터링·분석하여 "지금 당장 알아야 할 것"만 도메인별로 보여주는 멀티도메인 인텔리전스 대시보드.

핵심 설계 원칙: **도메인 추상화** — 수집/필터/분석 파이프라인은 도메인에 독립적이며, 새 도메인 추가 시 설정(KOL 리스트, 소스, 프롬프트 템플릿)만 등록하면 됨.

MVP 도메인: 🪙 Crypto + 🤖 AI/ML
MVP 범위: 도메인별 KOL 트윗 수집 + 뉴스/논문/GitHub 수집 + LLM 노이즈 필터링 + 도메인별 액션 시그널 + 통합 피드 대시보드 + 일일 다이제스트 + Telegram 알림.

## 2. 기술 스택
- **데이터 수집**: X API v2 (Filtered Stream + Search) + RSS 파서 (feedparser) + arXiv API + GitHub REST API + Whale Alert API + Dune API
- **실시간 처리**: Redis Streams (Kafka 대신 경량 선택)
- **AI 필터/분석**:
  - 노이즈 필터링: Google Gemini 2.0 Flash (빠르고 저렴, 도메인별 프롬프트 템플릿)
  - 심층 분석/요약: Anthropic Claude Sonnet (도메인별 분석 프롬프트)
- **백엔드**: Python 3.12 + FastAPI + APScheduler
- **DB**: Supabase (PostgreSQL)
- **프론트엔드**: Next.js 14 + TailwindCSS + Socket.io (실시간)
- **알림**: Telegram Bot API (python-telegram-bot)
- **배포**: Vercel (FE) + Railway (BE + Redis)

## 3. 디렉토리 구조
intel-hub/
├── backend/
│   ├── domains/
│   │   ├── __init__.py
│   │   ├── registry.py              # 도메인 레지스트리 (도메인 등록/조회)
│   │   ├── base.py                  # BaseDomainConfig 추상 클래스
│   │   ├── crypto/
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # 크립토 도메인 설정 (KOL, 소스, 프롬프트)
│   │   │   ├── kol_list.py          # 크립토 KOL 리스트
│   │   │   ├── prompts.py           # 크립토 전용 필터/분석 프롬프트
│   │   │   └── action_signals.py    # 크립토 액션 시그널 정의 (opportunity/watch/risk)
│   │   └── ai_ml/
│   │       ├── __init__.py
│   │       ├── config.py            # AI/ML 도메인 설정
│   │       ├── kol_list.py          # AI/ML KOL 리스트
│   │       ├── prompts.py           # AI/ML 전용 필터/분석 프롬프트
│   │       └── action_signals.py    # AI/ML 액션 시그널 정의 (apply/learn/paradigm_shift)
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py                  # BaseCollector 추상 클래스
│   │   ├── twitter.py               # X API v2 트윗 수집기 (도메인 공통)
│   │   ├── rss.py                   # RSS 뉴스 수집기 (도메인 공통)
│   │   ├── arxiv.py                 # arXiv 논문 수집기 (AI/ML 도메인)
│   │   ├── github.py                # GitHub trending 수집기 (AI/ML 도메인)
│   │   └── onchain.py               # Whale Alert / Dune 온체인 (크립토 도메인)
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── noise_filter.py          # LLM 노이즈 필터 (도메인별 프롬프트 로드)
│   │   ├── analyzer.py              # 심층 분석 (도메인별 프롬프트 로드)
│   │   ├── sentiment.py             # 센티먼트 스코어링
│   │   ├── action_signal.py         # 액션 시그널 분류 (도메인별 시그널 체계)
│   │   ├── cross_domain.py          # 크로스도메인 연결 분석
│   │   └── daily_digest.py          # 도메인별 일일 AI 요약
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI 앱
│   │   ├── routes/
│   │   │   ├── feed.py              # 통합/도메인별 실시간 피드 API
│   │   │   ├── domains.py           # 도메인 관리 API
│   │   │   ├── topics.py            # 도메인별 토픽 인텔리전스 (코인별/AI토픽별)
│   │   │   ├── kols.py              # KOL 관리 API
│   │   │   └── digest.py            # 일일 다이제스트
│   │   └── websocket.py             # 실시간 피드 WebSocket (도메인 채널 분리)
│   ├── telegram/
│   │   ├── __init__.py
│   │   └── bot.py                   # Telegram 알림 봇 (도메인별 구독)
│   ├── db/
│   │   └── migrations/001_init.sql
│   ├── config.py
│   └── scheduler.py                 # 도메인별 수집 스케줄러
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx             # 통합 피드 대시보드
│   │   │   ├── domain/[slug]/page.tsx    # 도메인별 피드
│   │   │   ├── topic/[domain]/[slug]/page.tsx  # 토픽별 인텔리전스 (코인별/AI토픽별)
│   │   │   ├── kols/page.tsx        # KOL 히트맵 (도메인 필터)
│   │   │   └── digest/page.tsx      # 일일 다이제스트 (도메인 탭)
│   │   ├── components/
│   │   │   ├── FeedItem.tsx         # 피드 아이템 카드
│   │   │   ├── FeedList.tsx         # 실시간 피드 리스트
│   │   │   ├── DomainTabs.tsx       # 도메인 탭 필터 (All / 🪙 / 🤖 / ...)
│   │   │   ├── TopicCard.tsx        # 토픽 인텔리전스 카드 (코인/AI토픽 공통)
│   │   │   ├── KolHeatmap.tsx       # KOL 발언 히트맵
│   │   │   ├── SentimentGauge.tsx   # 센티먼트 게이지
│   │   │   ├── ActionBadge.tsx      # 액션 시그널 배지 (도메인별 의미 다름)
│   │   │   ├── EventCalendar.tsx    # 통합 이벤트 캘린더
│   │   │   └── DigestView.tsx       # 일일 요약 뷰
│   │   └── lib/
│   │       ├── api.ts
│   │       └── socket.ts            # Socket.io 클라이언트
│   └── package.json
└── .env

## 4. 데이터베이스 스키마

-- 도메인 설정 (시스템 테이블)
create table domains (
  id text primary key,                     -- 'crypto', 'ai_ml' 등
  display_name text not null,              -- '🪙 Crypto', '🤖 AI/ML'
  description text,
  is_active boolean default true,
  config jsonb,                            -- 도메인별 추가 설정
  created_at timestamptz default now()
);

-- KOL 목록 (도메인별)
create table kols (
  id uuid default gen_random_uuid() primary key,
  domain_id text references domains(id) not null,
  twitter_username text not null,
  display_name text,
  follower_count int,
  credibility_score decimal(3,2) default 0.50,
  category text,                           -- 도메인마다 다른 카테고리 ('analyst'/'researcher'/'engineer' 등)
  is_active boolean default true,
  created_at timestamptz default now(),
  unique(domain_id, twitter_username)
);

-- 수집된 원본 아이템 (도메인 공통)
create table raw_items (
  id uuid default gen_random_uuid() primary key,
  domain_id text references domains(id) not null,
  source_type text not null,               -- 'twitter', 'news', 'onchain', 'arxiv', 'github'
  source_id text,                          -- 트윗 ID / 뉴스 URL / arXiv ID / GitHub repo
  author text,
  content text not null,
  url text,
  media_urls jsonb,
  raw_metadata jsonb,                      -- 소스별 메타데이터 (likes, stars, citations 등)
  collected_at timestamptz default now(),
  unique(domain_id, source_type, source_id)
);

-- AI 필터링/분석 결과 (도메인 공통)
create table analyzed_items (
  id uuid default gen_random_uuid() primary key,
  raw_item_id uuid references raw_items(id),
  domain_id text references domains(id) not null,
  is_signal boolean not null,
  noise_reason text,
  importance_score int check (importance_score between 1 and 10),
  sentiment_score int check (sentiment_score between -100 and 100),
  action_signal text not null,             -- 도메인별 시그널: crypto='watch'|'opportunity'|'risk'|'neutral', ai_ml='apply'|'learn'|'paradigm_shift'|'neutral'
  context_summary text,
  related_topics text[],                   -- 관련 토픽 (crypto: ['BTC','SOL'], ai_ml: ['LLM','Agent'])
  category text,                           -- 도메인별 카테고리
  llm_model text,
  analyzed_at timestamptz default now()
);

-- 토픽별 일일 요약 (도메인 공통)
create table daily_digests (
  id uuid default gen_random_uuid() primary key,
  domain_id text references domains(id) not null,
  topic text not null,                     -- crypto: 'BTC'|'SOL', ai_ml: 'LLM'|'Agent'|'Vision'
  digest_date date not null,
  summary text not null,
  detailed_analysis text,
  sentiment_avg int,
  signal_count int,
  top_events jsonb,
  created_at timestamptz default now(),
  unique(domain_id, topic, digest_date)
);

-- 크로스도메인 연결 분석
create table cross_domain_links (
  id uuid default gen_random_uuid() primary key,
  source_item_id uuid references analyzed_items(id),
  target_item_id uuid references analyzed_items(id),
  link_type text,                          -- 'causal', 'related', 'contradicts'
  explanation text,                        -- AI 생성 연결 설명
  confidence decimal(3,2),
  created_at timestamptz default now()
);

-- Telegram 구독자 (도메인별 필터)
create table telegram_subscribers (
  id uuid default gen_random_uuid() primary key,
  chat_id bigint unique not null,
  username text,
  alert_level text default 'high' check (alert_level in ('all', 'high', 'critical')),
  domain_filter text[],                    -- 구독 도메인 ['crypto', 'ai_ml'] (null=전체)
  topic_filter text[],                     -- 특정 토픽만 알림 (null=전체)
  is_active boolean default true,
  created_at timestamptz default now()
);

## 5. 도메인 설정 시스템

### 5-1. 도메인 레지스트리 (domains/registry.py)
- 싱글톤 패턴으로 도메인 설정 관리
- 각 도메인은 BaseDomainConfig를 상속:
  - kol_list: KOL 리스트
  - rss_sources: RSS 소스 URL 리스트
  - collectors: 해당 도메인에 사용할 수집기 클래스 리스트
  - noise_filter_prompt: 노이즈 필터 프롬프트 템플릿
  - analyzer_prompt: 심층 분석 프롬프트 템플릿
  - action_signals: 액션 시그널 정의 (이름, 아이콘, 설명)
  - categories: 카테고리 리스트
  - topics: 트래킹할 토픽 리스트
- 새 도메인 추가 = 새 폴더 + config.py 작성 + registry에 등록

### 5-2. 크립토 도메인 설정 (domains/crypto/)
- KOL 리스트 (20명):
  - Tier 1: @colouredcoins, @Pentosh1, @CryptoKaleo, @blknoiz06, @Ansem
  - Tier 2: @Cryptoyieldinfo, @Maboroshi_Yuki, @inversebrah, @CryptoBullet1
  - Tier 3: @WuBlockchain, @zachxbt, @DefiIgnas
  - (동적 추가/제거 가능)
- RSS 소스: CoinDesk, The Block, Decrypt, CoinTelegraph
- 수집기: TwitterCollector, RSSCollector, OnchainCollector
- 액션 시그널:
  - 🟢 opportunity: 매수/참여 기회
  - 🟡 watch: 주시 필요
  - 🔴 risk: 리스크 경고
  - ⚪ neutral: 정보성
- 카테고리: price_action, regulation, partnership, technical, macro, airdrop, hack, other
- 토픽: BTC, ETH, SOL, SUI 등 주요 코인

### 5-3. AI/ML 도메인 설정 (domains/ai_ml/)
- KOL 리스트 (15명):
  - Tier 1 (속보): @TestingCatalog, @_akhaliq, @DrJimFan, @kaboroMatt
  - Tier 2 (분석/연구): @swyx, @AndrewYNg, @ylecun, @hardmaru
  - Tier 3 (실무): @laboroai, @huggingface, @OpenAI, @AnthropicAI
  - (동적 추가/제거 가능)
- RSS 소스: OpenAI Blog, Anthropic Research, Google DeepMind Blog, HuggingFace Blog, The Gradient, Import AI (Jack Clark)
- 수집기: TwitterCollector, RSSCollector, ArxivCollector, GitHubCollector
- 액션 시그널:
  - 🟢 apply: 내 프로젝트에 바로 적용 가능
  - 🟡 learn: 학습 필요, 트렌드 파악
  - 🔴 paradigm_shift: 패러다임 전환, 전략 재검토 필요
  - ⚪ neutral: 정보성
- 카테고리: model_release, paper, tool, framework, regulation, benchmark, dataset, open_source, other
- 토픽: LLM, Agent, Vision, Multimodal, Safety, Infra, Open Source 등

## 6. 수집기 구현 상세

### 6-1. 트윗 수집기 (collectors/twitter.py) — 도메인 공통
- X API v2 Search Recent endpoint로 도메인별 KOL 트윗 주기적 수집 (5분 간격)
- 쿼리: `from:{username}` 각 KOL별
- 도메인별 KOL 리스트를 domain registry에서 로드
- 수집 데이터: 트윗 본문, 인용 트윗, 미디어, 좋아요/리트윗 수, 시간
- 중복 방지: (domain_id, source_type, source_id) unique constraint
- Rate limit 관리: 15분당 450 요청 제한 준수, 도메인 간 KOL 수집 통합 배치

### 6-2. RSS 뉴스 수집기 (collectors/rss.py) — 도메인 공통
- 도메인별 RSS 소스 리스트를 domain registry에서 로드
- 5분 간격 폴링, feedparser 사용
- 헤드라인 + 요약문 + URL 저장

### 6-3. arXiv 수집기 (collectors/arxiv.py) — AI/ML 도메인
- arXiv API로 cs.AI, cs.CL, cs.LG 카테고리 daily papers 수집
- 하루 1회 배치 수집 (09:00 KST)
- 제목, 저자, 초록, arXiv URL 저장
- raw_metadata에 카테고리, citation count 등 포함

### 6-4. GitHub 수집기 (collectors/github.py) — AI/ML 도메인
- GitHub REST API로 trending repos 수집 (Python, ML 태그)
- 주요 오픈소스 릴리즈 모니터링 (llama.cpp, vllm, transformers, langchain 등)
- 6시간 간격 배치 수집
- 스타 수, 포크 수, 최신 릴리즈 노트 저장

### 6-5. 온체인 수집기 (collectors/onchain.py) — 크립토 도메인
- Whale Alert API: 고래 지갑 대량 이동 감지
- Dune API: 커스텀 쿼리 기반 온체인 시그널
- 5분 간격 폴링

## 7. AI 파이프라인 구현 상세

### 7-1. 도메인별 노이즈 필터 (pipeline/noise_filter.py)
- domain registry에서 해당 도메인의 noise_filter_prompt 로드
- Gemini Flash로 실행
- 출력 형식은 도메인 공통 JSON:
{
  "is_signal": true/false,
  "noise_reason": "only if noise",
  "importance_score": 1-10,
  "related_topics": ["BTC", "SOL"] 또는 ["LLM", "Agent"],
  "category": "도메인별 카테고리",
  "context_summary": "왜 중요한지 한국어 1문장"
}

**크립토 노이즈 필터 프롬프트:**
You are a crypto intelligence filter. Classify this content as SIGNAL or NOISE.
SIGNAL = Actionable alpha, market-moving info, genuine analysis, important crypto updates.
NOISE = Shilling, paid promotion, vague sentiment ("bullish vibes"), memes, engagement farming.
Content: {content}
Author: {author} (Credibility: {credibility_score})
Source: {source_type}
Output JSON with: is_signal, noise_reason, importance_score (1-10), related_topics (coin symbols), category (price_action|regulation|partnership|technical|macro|airdrop|hack|other), context_summary (한국어 1문장)

**AI/ML 노이즈 필터 프롬프트:**
You are an AI/ML intelligence filter. Classify this content as SIGNAL or NOISE.
SIGNAL = New model release, significant paper, useful tool/framework, important benchmark, industry shift, practical technique.
NOISE = Hype without substance, rehashed news, vague predictions, self-promotion, engagement farming, minor updates.
Content: {content}
Author: {author} (Credibility: {credibility_score})
Source: {source_type} (twitter|news|arxiv|github)
Output JSON with: is_signal, noise_reason, importance_score (1-10), related_topics (e.g. ["LLM","Agent"]), category (model_release|paper|tool|framework|regulation|benchmark|dataset|open_source|other), context_summary (한국어 1문장)

### 7-2. 도메인별 심층 분석 (pipeline/analyzer.py)
importance_score >= 7인 아이템에 대해 Claude Sonnet으로 추가 분석.
domain registry에서 analyzer_prompt 로드.

**크립토 심층 분석 프롬프트:**
이 크립토 콘텐츠를 심층 분석하라:
원문: {content}
작성자: {author} | 소스: {source_type}
관련 코인: {related_topics}
분석:
1. 시장 영향 (단기/중기)
2. 센티먼트 스코어 (-100 ~ +100, 근거)
3. 액션 시그널: 🟢 opportunity / 🟡 watch / 🔴 risk / ⚪ neutral
4. 관련 맥락: 이전 유사 이벤트와 연결
Output JSON: { "sentiment_score": 0, "action_signal": "", "analysis": "2-3문장 한국어" }

**AI/ML 심층 분석 프롬프트:**
이 AI/ML 콘텐츠를 심층 분석하라:
원문: {content}
작성자: {author} | 소스: {source_type}
관련 토픽: {related_topics}
분석:
1. 기술적 중요성 (혁신도, 기존 방법 대비 개선)
2. 실용적 적용 가능성 (바로 써먹을 수 있는지, 어떤 프로젝트에)
3. 센티먼트 스코어 (-100 ~ +100, 커뮤니티 반응 기반)
4. 액션 시그널: 🟢 apply (바로 적용) / 🟡 learn (학습 필요) / 🔴 paradigm_shift (전략 재검토) / ⚪ neutral
5. 관련 맥락: 경쟁 모델/도구와 비교, 트렌드 방향
Output JSON: { "sentiment_score": 0, "action_signal": "", "analysis": "2-3문장 한국어" }

### 7-3. 크로스도메인 연결 분석 (pipeline/cross_domain.py)
- 30분 간격으로 최근 analyzed_items를 도메인 간 매칭
- 예: "AI 칩 수출 규제" (ai_ml) ↔ "AI 관련 크립토 토큰 하락" (crypto)
- Claude Sonnet으로 연결 타입(causal/related/contradicts) + 설명 생성
- cross_domain_links 테이블에 저장

### 7-4. 도메인별 일일 다이제스트 (pipeline/daily_digest.py)
- 매일 09:00 KST 실행 (APScheduler)
- 도메인별로 전일 24시간 analyzed_items를 토픽별 그루핑
- Claude Sonnet으로 토픽별 요약 생성:
  - 크립토: "지난 24시간 {coin_symbol} 관련 주요 이벤트" → 1줄 요약 + 3줄 분석
  - AI/ML: "지난 24시간 {topic} 관련 주요 이벤트" → 1줄 요약 + 3줄 분석
- 크로스도메인 하이라이트도 포함

## 8. Telegram 봇 (telegram/bot.py)
- /start: 구독 시작
- /domains: 구독 도메인 설정 (crypto, ai_ml, all)
- /alert {level}: 알림 레벨 설정 (all/high/critical)
- /topics {BTC,SOL,LLM,Agent}: 관심 토픽 필터
- /digest: 오늘의 다이제스트 즉시 수신 (도메인별)
- 자동 알림: importance_score >= 8 또는 high-risk 시그널일 때
- 메시지 포맷 (도메인 태그 포함):
🪙 🔴 [RISK] SOL 관련 긴급
📡 @zachxbt: "Solana의 X 프로토콜에서 익스플로잇 발생..."
💡 SOL 가격에 단기 하방 압력 가능.
🔗 원문: {url}

🤖 🟢 [APPLY] LLM Agent 관련
📡 @_akhaliq: "OpenAI releases new function calling API..."
💡 기존 Agent 파이프라인에 바로 적용 가능. 응답 정확도 40% 향상.
🔗 원문: {url}

## 9. 프론트엔드 주요 컴포넌트
- **DomainTabs**: 도메인 탭 필터 — All / 🪙 Crypto / 🤖 AI·ML (향후 확장 가능)
- **FeedList**: 통합 실시간 피드 — WebSocket, 도메인 필터 + importance 순 정렬
- **FeedItem**: 카드 — 도메인 태그, 작성자, 내용, AI 요약, 액션 배지, 센티먼트 바
- **TopicCard**: 토픽별 인텔리전스 — 도메인 공통 컴포넌트 (코인/AI토픽 모두 렌더링)
- **KolHeatmap**: 도메인별 KOL 발언 빈도+센티먼트 히트맵
- **EventCalendar**: 통합 이벤트 캘린더 (크립토: 토큰 언락 / AI: 모델 출시 등)
- **ActionBadge**: 도메인별 액션 시그널 배지 (크립토 🟢=기회, AI 🟢=적용 등)
- 다크 테마 기본, TailwindCSS, 도메인별 액센트 컬러 (크립토=골드, AI=퍼플)

## 10. 환경 변수 (.env)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
ANTHROPIC_API_KEY=your_claude_key
GOOGLE_AI_API_KEY=your_gemini_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
REDIS_URL=redis://localhost:6379
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GITHUB_TOKEN=your_github_token  # GitHub API rate limit 완화용

## 11. 구현 순서 (Phase별)
### Phase 1: 코어 + 크립토 (Week 1-3)
1. 프로젝트 초기화 (Python backend + Next.js frontend)
2. 도메인 레지스트리 + BaseDomainConfig 설계
3. DB 스키마 마이그레이션 (domain 필드 포함)
4. 크립토 도메인 설정 + KOL 시드 데이터
5. Twitter 수집기 (도메인 공통) + RSS 수집기 (도메인 공통)
6. 온체인 수집기 (크립토)
7. 도메인별 노이즈 필터 파이프라인 (Gemini Flash)
8. 도메인별 심층 분석 + 센티먼트 (Claude Sonnet)
9. 크립토 일일 다이제스트
10. Telegram 봇 (도메인별 구독/필터)

### Phase 2: AI/ML 도메인 (Week 3-5)
11. AI/ML 도메인 설정 + KOL 시드 데이터
12. arXiv 수집기 + GitHub 수집기
13. AI/ML 노이즈 필터 프롬프트 + 분석 프롬프트
14. AI/ML 액션 시그널 (apply/learn/paradigm_shift)
15. AI/ML 일일 다이제스트
16. 크로스도메인 연결 분석 기본

### Phase 3: 통합 UI (Week 4-6)
17. 통합 피드 대시보드 + 도메인 탭
18. 토픽별 인텔리전스 페이지
19. KOL 히트맵 (도메인 통합)
20. 통합 이벤트 캘린더
21. 통합 테스트 + 배포

## 12. 주의사항
- **X API 비용**: Basic tier $100/월 — 도메인 간 KOL 수집 통합 배치로 최적화
- **노이즈 필터 정확도가 생명**: 도메인별 수동 검증으로 프롬프트 튜닝, false positive/negative 추적
- **도메인 추상화 유지**: 새 도메인 추가 시 코드 변경 최소화되도록 인터페이스 엄격하게 관리
- **KOL 신뢰도 동적 업데이트**: 예측 정확도 기반 credibility_score 조정
- **Rate limiting**: 모든 외부 API에 레이트 리미터 적용 (Redis 기반)
- **비용 관리**: LLM 호출 비용 도메인별 일일 로깅, importance_score 낮은 건 분석 스킵
- **arXiv/GitHub**: daily/6h batch 수집 — 실시간 불필요, rate limit 여유
- **원문 링크 필수**: 모든 요약/분석에 원문 URL 첨부 (저작권 fair use)
```