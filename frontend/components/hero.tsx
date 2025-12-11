'use client'

import { motion } from 'framer-motion'
import { Button } from './ui/button'
import { ArrowRight, Sparkles } from 'lucide-react'

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-primary/10 to-background py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col items-center text-center"
        >
          <div className="mb-4 inline-flex items-center rounded-full border px-4 py-1.5 text-sm">
            <Sparkles className="mr-2 h-4 w-4 text-primary" />
            AI-Powered Recommendations
          </div>

          <h1 className="mb-6 max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            Discover Products{' '}
            <span className="text-primary">Tailored Just for You</span>
          </h1>

          <p className="mb-8 max-w-2xl text-lg text-muted-foreground">
            Experience shopping like never before with our advanced AI recommendation engine.
            Get personalized product suggestions based on your preferences and behavior.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button size="lg" className="group">
              Explore Products
              <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Button>
            <Button size="lg" variant="outline">
              View Recommendations
            </Button>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-3 gap-8">
            <div>
              <div className="text-3xl font-bold text-primary">100+</div>
              <div className="text-sm text-muted-foreground">Products</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">95%</div>
              <div className="text-sm text-muted-foreground">Accuracy</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">50+</div>
              <div className="text-sm text-muted-foreground">Happy Users</div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Background decoration */}
      <div className="absolute inset-0 -z-10 opacity-20">
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-secondary rounded-full blur-3xl" />
      </div>
    </section>
  )
}
