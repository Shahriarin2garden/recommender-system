import dynamic from 'next/dynamic'
import { Hero } from '@/components/hero'

// Skeleton placeholders
const ProductSkeleton = () => (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    {[...Array(8)].map((_, i) => (
      <div key={i} className="space-y-3">
        <div className="aspect-square w-full skeleton rounded-2xl" />
        <div className="h-3.5 w-3/4 skeleton" />
        <div className="h-3 w-1/2 skeleton" />
      </div>
    ))}
  </div>
)

const RecommendSkeleton = () => (
  <div>
    <div className="h-8 w-52 skeleton mb-8" />
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="space-y-3">
          <div className="aspect-square w-full skeleton rounded-2xl" />
          <div className="h-3.5 w-3/4 skeleton" />
          <div className="h-3 w-1/2 skeleton" />
        </div>
      ))}
    </div>
  </div>
)

const ProductGrid = dynamic(
  () => import('@/components/product-grid').then((mod) => ({ default: mod.ProductGrid })),
  { loading: () => <ProductSkeleton /> }
)

const RecommendationSection = dynamic(
  () => import('@/lib/recommendation-section').then((mod) => ({ default: mod.RecommendationSection })),
  { loading: () => <RecommendSkeleton /> }
)

export default function Home() {
  return (
    <div className="flex flex-col">

      {/* Hero + how-it-works */}
      <Hero />

      {/* Recommended for You */}
      <section
        id="recommended-products"
        className="container mx-auto px-6 lg:px-8 py-20 sm:py-28"
      >
        <RecommendationSection userId={1} />
      </section>

      {/* Divider */}
      <div className="container mx-auto px-6 lg:px-8">
        <div className="h-px bg-border/50" />
      </div>

      {/* All Products */}
      <section
        id="all-products"
        className="container mx-auto px-6 lg:px-8 py-20 sm:py-28"
      >
        <div className="mb-12">
          <p className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-3">Catalogue</p>
          <h2 className="text-4xl sm:text-5xl font-bold tracking-tight">Explore All</h2>
        </div>
        <ProductGrid />
      </section>

    </div>
  )
}
