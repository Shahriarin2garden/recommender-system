import dynamic from 'next/dynamic'
import { Hero } from '@/components/hero'

// Dynamically import heavy components for better performance
const ProductGrid = dynamic(() => import('@/components/product-grid').then(mod => ({ default: mod.ProductGrid })), {
  loading: () => (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      {[...Array(8)].map((_, i) => (
        <div key={i} className="animate-pulse space-y-4">
          <div className="aspect-square w-full rounded-2xl bg-muted/50" />
          <div className="h-4 w-3/4 bg-muted/50 rounded" />
          <div className="h-4 w-1/2 bg-muted/50 rounded" />
        </div>
      ))}
    </div>
  )
})

const RecommendationSection = dynamic(() => import('@/lib/recommendation-section').then(mod => ({ default: mod.RecommendationSection })), {
  loading: () => (
    <div>
      <div className="h-12 w-64 bg-muted/50 rounded-xl mb-10 animate-pulse" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="animate-pulse space-y-4">
            <div className="aspect-square w-full rounded-2xl bg-muted/50" />
            <div className="h-4 w-3/4 bg-muted/50 rounded" />
            <div className="h-4 w-1/2 bg-muted/50 rounded" />
          </div>
        ))}
      </div>
    </div>
  )
})

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <Hero />

      {/* Recommended for You */}
      <section className="container mx-auto px-6 lg:px-8 py-16 sm:py-20">
        <RecommendationSection userId={1} />
      </section>

      {/* All Products */}
      <section className="container mx-auto px-6 lg:px-8 py-16 sm:py-20 bg-muted/20">
        <h2 className="mb-10 text-4xl sm:text-5xl font-bold tracking-tight">Explore All</h2>
        <ProductGrid />
      </section>
    </div>
  )
}
