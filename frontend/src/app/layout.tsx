import type { Metadata } from "next";
import { Noto_Sans_KR, Space_Grotesk } from "next/font/google";

import "@/app/globals.css";

const heading = Space_Grotesk({ subsets: ["latin"], variable: "--font-heading" });
const body = Noto_Sans_KR({ subsets: ["latin"], variable: "--font-body" });

export const metadata: Metadata = {
  title: "Personal Intelligence Hub",
  description: "AI 기반 멀티도메인 인텔리전스 대시보드"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className="dark">
      <body className={`${heading.variable} ${body.variable} bg-background text-foreground antialiased`}>
        <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
      </body>
    </html>
  );
}
