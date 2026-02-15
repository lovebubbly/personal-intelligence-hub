"use client";

import { AnimatePresence } from "framer-motion";

import { FeedItem } from "@/components/FeedItem";
import { FeedItem as FeedItemType } from "@/types";

interface FeedListProps {
  items: FeedItemType[];
}

export function FeedList({ items }: FeedListProps) {
  return (
    <div className="space-y-3" data-testid="feed-list" aria-live="polite" aria-busy="false">
      <AnimatePresence initial={false}>
        {items.map((item) => (
          <FeedItem key={item.id} item={item} />
        ))}
      </AnimatePresence>
    </div>
  );
}
