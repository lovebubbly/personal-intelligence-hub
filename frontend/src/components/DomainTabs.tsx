"use client";

import { Button } from "@/components/ui/Button";
import { DomainId } from "@/types";

interface DomainTabsProps {
  value: DomainId;
  onChange: (value: DomainId) => void;
  options?: DomainId[];
}

const labels: Record<DomainId, string> = {
  all: "All",
  crypto: "🪙 Crypto",
  ai_ml: "🤖 AI/ML"
};

export function DomainTabs({ value, onChange, options = ["all", "crypto", "ai_ml"] }: DomainTabsProps) {
  return (
    <div className="flex flex-wrap items-center gap-2" role="tablist" aria-label="도메인 탭">
      {options.map((option) => (
        <Button
          key={option}
          variant={value === option ? "primary" : "outline"}
          size="sm"
          role="tab"
          aria-selected={value === option}
          aria-current={value === option}
          aria-label={`${labels[option]} 탭`}
          onClick={() => onChange(option)}
          data-testid={`domain-tab-${option}`}
        >
          {labels[option]}
        </Button>
      ))}
    </div>
  );
}
