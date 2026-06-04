'use client'

import Link from 'next/link'
import { Button } from './ui/button'
import { ArrowRight, Sparkles } from 'lucide-react'

const TICKER_ITEMS = [
  'AI-Powered Recommendations',
  'Personalized For You',
  'Collaborative Filtering',
  'Real-Time Discovery',
  'Matrix Factorization',
  'Neural Intelligence',
]

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-background">

      {/* ── Main Hero ── */}
      <div className="relative min-h-[92vh] flex flex-col items-center justify-center">

        {/* Ambient background blobs */}
        <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-[15%] left-[10%]  w-[500px] h-[500px] rounded-full bg-foreground/[0.03] blur-[120px]" />
          <div className="absolute bottom-[10%] right-[8%] w-[400px] h-[400px] rounded-full bg-foreground/[0.03] blur-[100px]" />
        </div>

        <div className="container mx-auto px-6 lg:px-8 flex flex-col items-center text-center">

          {/* Eyebrow badge */}
          <div
            className="inline-flex items-center gap-2 mb-8 px-4 py-1.5 rounded-full border border-border/60 bg-muted/40 text-xs font-medium text-muted-foreground animate-fade-in"
            style={{ animationDelay: '0ms' }}
          >
            <Sparkles className="h-3 w-3" />
            <span>AI-Powered Recommendations</span>
          </div>

          {/* Giant headline — exaggerated minimalism */}
          <h1
            className="text-[clamp(3.5rem,12vw,9rem)] font-bold tracking-[-0.04em] leading-[0.9] mb-8 animate-fade-in"
            style={{ animationDelay: '80ms' }}
          >
            <span className="block">Discover.</span>
            <span className="block animate-gradient-text">Personalized.</span>
          </h1>

          {/* Subheadline */}
          <p
            className="text-base sm:text-lg md:text-xl text-muted-foreground max-w-xl mb-12 font-light leading-relaxed animate-fade-in"
            style={{ animationDelay: '160ms' }}
          >
            Products curated by machine learning.
            <br className="hidden sm:block" />
            Every recommendation made just for you.
          </p>

          {/* CTAs */}
          <div
            className="flex flex-col sm:flex-row gap-3 mb-20 animate-fade-in"
            style={{ animationDelay: '240ms' }}
          >
            <Button
              asChild
              size="lg"
              className="rounded-full px-8 h-12 text-sm font-medium bg-foreground text-background hover:bg-foreground/85 transition-all duration-300 group shadow-none"
            >
              <Link href="#all-products">
                Start Shopping
                <ArrowRight className="ml-2 h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
              </Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="rounded-full px-8 h-12 text-sm font-medium border-border/60 hover:bg-muted/60 transition-all duration-300 shadow-none"
            >
              <Link href="#recommended-products">View Picks</Link>
            </Button>
          </div>

          {/* Stats row */}
          <div
            className="flex items-center gap-10 sm:gap-16 animate-fade-in"
            style={{ animationDelay: '320ms' }}
          >
            {[
              { value: '100+', label: 'Products' },
              { value: '95%',  label: 'Accuracy' },
              { value: '50+',  label: 'Users' },
            ].map((stat, i) => (
              <div key={i} className="flex flex-col items-center gap-1">
                <span className="text-3xl sm:text-4xl font-bold tracking-tight tabular-nums">
                  {stat.value}
                </span>
                <span className="text-xs text-muted-foreground tracking-widest uppercase">
                  {stat.label}
                </span>
              </div>
            ))}
          </div>

        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-muted-foreground/50">
          <div className="w-px h-10 bg-gradient-to-b from-transparent via-border to-transparent" />
          <span className="text-[10px] tracking-[0.2em] uppercase">Scroll</span>
        </div>
      </div>

      {/* ── Marquee ticker ── */}
      <div className="border-y border-border/40 bg-muted/20 overflow-hidden py-3.5 select-none">
        <div className="flex animate-marquee whitespace-nowrap">
          {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, i) => (
            <span key={i} className="inline-flex items-center gap-4 mx-6 text-xs font-medium text-muted-foreground tracking-widest uppercase">
              <span className="w-1 h-1 rounded-full bg-muted-foreground/40 shrink-0" />
              {item}
            </span>
          ))}
        </div>
      </div>

      {/* ── How It Works strip ── */}
      <div className="container mx-auto px-6 lg:px-8 py-24 sm:py-32">
        <div className="text-center mb-16">
          <p className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-4">How it works</p>
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight">
            Intelligence, built in.
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-px bg-border/40 rounded-2xl overflow-hidden stagger">
          {[
            {
              step: '01',
              title: 'Browse & Interact',
              desc: 'Explore products naturally. Every click and view shapes your profile silently.',
            },
            {
              step: '02',
              title: 'AI Learns You',
              desc: 'Collaborative filtering and matrix factorization build your taste model in real-time.',
            },
            {
              step: '03',
              title: 'Curated Discovery',
              desc: 'Receive a ranked feed of products tailored precisely to your preferences.',
            },
          ].map((item) => (
            <div
              key={item.step}
              className="bg-background p-8 sm:p-10 flex flex-col gap-4 group hover:bg-muted/30 transition-colors duration-300"
            >
              <span className="text-[10px] tracking-[0.3em] text-muted-foreground/50 uppercase font-medium">
                {item.step}
              </span>
              <h3 className="text-lg font-semibold tracking-tight">{item.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

    </section>
  )
}
