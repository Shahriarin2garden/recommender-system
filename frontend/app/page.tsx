import { Hero } from '@/components/hero'
import { ProductGrid } from '@/components/product-grid'
import { RecommendationSection } from '@/lib/recommendation-section'

export default function Home() {
  return (
    <div className="flex flex-col gap-12 pb-12">
      {/* Hero Section */}
      <Hero />

      {/* Recommended for You */}
      <section className="container mx-auto px-4">
        <RecommendationSection userId={1} />
      </section>

      {/* All Products */}
      <section className="container mx-auto px-4">
        <h2 className="mb-6 text-3xl font-bold">All Products</h2>
        <ProductGrid />
      </section>
    </div>
  )
}
