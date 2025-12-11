'use client'

import { Button } from './ui/button'
import { ArrowRight } from 'lucide-react'

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-background">
      {/* Full-width hero with centered content */}
      <div className="relative min-h-[85vh] flex items-center justify-center">
        <div className="container mx-auto px-6 lg:px-8 flex flex-col items-center text-center z-10 animate-fade-in">
          {/* Main headline - Apple/Nike style */}
          <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight mb-6 leading-tight">
            Discover.
            <br />
            <span className="text-foreground/60">Personalized.</span>
          </h1>

          <p className="text-lg sm:text-xl md:text-2xl text-muted-foreground max-w-3xl mb-12 font-light">
            AI-powered recommendations that understand you.
            <br className="hidden sm:block" />
            Every product, curated for your style.
          </p>

          {/* CTA Buttons - Minimal style */}
          <div className="flex flex-col sm:flex-row gap-4 mb-16">
            <Button 
              size="lg" 
              className="rounded-full px-8 py-6 text-base font-medium bg-foreground text-background hover:bg-foreground/90 transition-all duration-300 group"
            >
              Shop Now
              <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Button>
            <Button 
              size="lg" 
              variant="ghost"
              className="rounded-full px-8 py-6 text-base font-medium hover:bg-foreground/5 transition-all duration-300"
            >
              Learn More
            </Button>
          </div>

          {/* Minimal stats with dividers */}
          <div className="flex items-center gap-8 sm:gap-12 text-sm sm:text-base">
            <div className="flex flex-col items-center">
              <div className="text-2xl sm:text-3xl font-semibold mb-1">100+</div>
              <div className="text-muted-foreground font-light">Products</div>
            </div>
            <div className="h-12 w-px bg-border" />
            <div className="flex flex-col items-center">
              <div className="text-2xl sm:text-3xl font-semibold mb-1">95%</div>
              <div className="text-muted-foreground font-light">Accuracy</div>
            </div>
            <div className="h-12 w-px bg-border" />
            <div className="flex flex-col items-center">
              <div className="text-2xl sm:text-3xl font-semibold mb-1">50+</div>
              <div className="text-muted-foreground font-light">Users</div>
            </div>
          </div>
        </div>

        {/* Subtle gradient background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
        </div>
      </div>
    </section>
  )
}
