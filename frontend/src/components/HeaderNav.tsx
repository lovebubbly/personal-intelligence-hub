import Link from "next/link";

const navItems = [
  { href: "/", label: "Feed" },
  { href: "/domain/crypto", label: "Crypto" },
  { href: "/domain/ai_ml", label: "AI/ML" },
  { href: "/digest", label: "Digest" },
  { href: "/kols", label: "KOLs" }
];

export function HeaderNav() {
  return (
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4 border-b border-border/70 pb-5">
      <div>
        <p className="text-xs tracking-[0.18em] text-amber-300/80">MULTI-DOMAIN INTELLIGENCE</p>
        <p className="text-sm text-muted">Capture to Signal to Action</p>
      </div>
      <nav className="flex flex-wrap items-center gap-2 text-sm">
        {navItems.map((item) => (
          <Link key={item.href} className="rounded-xl border border-border px-3 py-2 hover:border-amber-300/70" href={item.href}>
            {item.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
