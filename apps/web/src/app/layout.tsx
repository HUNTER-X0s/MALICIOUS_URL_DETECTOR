import type { Metadata } from 'next';
import './globals.css';
import { Header } from '@/components/layout/header';
import { Footer } from '@/components/layout/footer';

export const metadata: Metadata = {
  title: 'URLSentinel — Security-First Malicious URL Detection Platform',
  description: 'Zero-trust real-time protection against malicious URLs, phishing portals, brand impersonation, and deceptive redirects.',
  keywords: ['URL scanner', 'phishing detector', 'malicious link protection', 'cybersecurity', 'browser extension', 'zero trust'],
  authors: [{ name: 'URLSentinel Autonomous Engineering' }],
  robots: 'index, follow',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col font-sans selection:bg-indigo-500/30 selection:text-white" suppressHydrationWarning>
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}

