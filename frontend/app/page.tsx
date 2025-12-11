import { Hero } from '@/components/hero'
import { ProductGrid } from '@/components/product-grid'
import { RecommendationSection } from '@/lib/recommendation-section'

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
