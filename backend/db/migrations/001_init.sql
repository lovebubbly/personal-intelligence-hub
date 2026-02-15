-- Initial schema for Personal Intelligence Hub MVP

create table if not exists domains (
  id text primary key,
  display_name text not null,
  description text,
  is_active boolean default true,
  config jsonb,
  created_at timestamptz default now()
);

create table if not exists kols (
  id uuid default gen_random_uuid() primary key,
  domain_id text references domains(id) not null,
  twitter_username text not null,
  display_name text,
  follower_count int,
  credibility_score decimal(3,2) default 0.50,
  category text,
  is_active boolean default true,
  created_at timestamptz default now(),
  unique(domain_id, twitter_username)
);

create table if not exists raw_items (
  id uuid default gen_random_uuid() primary key,
  domain_id text references domains(id) not null,
  source_type text not null,
  source_id text,
  author text,
  content text not null,
  url text,
  media_urls jsonb,
  raw_metadata jsonb,
  collected_at timestamptz default now(),
  unique(domain_id, source_type, source_id)
);
create index if not exists ix_raw_items_domain_collected on raw_items(domain_id, collected_at desc);

create table if not exists analyzed_items (
  id uuid default gen_random_uuid() primary key,
  raw_item_id uuid references raw_items(id) not null,
  domain_id text references domains(id) not null,
  is_signal boolean not null,
  noise_reason text,
  importance_score int check (importance_score between 1 and 10),
  sentiment_score int check (sentiment_score between -100 and 100),
  action_signal text not null,
  context_summary text,
  related_topics text[],
  category text,
  llm_model text,
  analyzed_at timestamptz default now(),
  unique(raw_item_id)
);
create index if not exists ix_analyzed_domain_analyzed on analyzed_items(domain_id, analyzed_at desc);
create index if not exists ix_analyzed_importance_analyzed on analyzed_items(importance_score desc, analyzed_at desc);

create table if not exists daily_digests (
  id uuid default gen_random_uuid() primary key,
  domain_id text references domains(id) not null,
  topic text not null,
  digest_date date not null,
  summary text not null,
  detailed_analysis text,
  sentiment_avg int,
  signal_count int,
  top_events jsonb,
  created_at timestamptz default now(),
  unique(domain_id, topic, digest_date)
);
create index if not exists ix_daily_digests_domain_date on daily_digests(domain_id, digest_date);

create table if not exists cross_domain_links (
  id uuid default gen_random_uuid() primary key,
  source_item_id uuid references analyzed_items(id),
  target_item_id uuid references analyzed_items(id),
  link_type text,
  explanation text,
  confidence decimal(3,2),
  created_at timestamptz default now()
);

create table if not exists telegram_subscribers (
  id uuid default gen_random_uuid() primary key,
  chat_id bigint unique not null,
  username text,
  alert_level text default 'high' check (alert_level in ('all', 'high', 'critical')),
  domain_filter text[],
  topic_filter text[],
  is_active boolean default true,
  created_at timestamptz default now()
);

create table if not exists model_usage_daily (
  id uuid default gen_random_uuid() primary key,
  usage_date date not null,
  model text not null,
  calls int default 0,
  tokens_in int default 0,
  tokens_out int default 0,
  cost_estimate decimal(10,4) default 0,
  created_at timestamptz default now(),
  unique(usage_date, model)
);
