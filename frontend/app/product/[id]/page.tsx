'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowLeft, ShoppingBag, Heart, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { ProductCard } from '@/components/product-card'
import { apiClient } from '@/lib/api-client'

interface Product {
  id: number
  name: string
  description?: string
  price?: number
  category: string
  image_url?: string | null
  tags?: string
  stock_quantity?: number
}

export default function ProductDetailPage() {
  const params = useParams()
  const router = useRouter()
  const productId = Number(params.id)

  const [product, setProduct] = useState<Product | null>(null)
  const [similar, setSimilar] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    const load = async () => {
      try {
        const [prod, simData] = await Promise.all([
          apiClient.getProductById(productId),
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/v1/similar/${productId}`)
            .then(r => r.ok ? r.json() : { similar_products: [] })
        ])
        setProduct(prod)
        setSimilar(simData.similar_products?.map((r: any) => r.product) ?? [])
      } catch (e: any) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [productId])

  const handleAddToBag = async () => {
    await apiClient.trackClick(1, productId)
    setAdded(true)
    setTimeout(() => setAdded(false), 2000)
  }

  if (loading) {
    return (
      <div className="container mx-auto px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <Skeleton className="aspect-square rounded-3xl" />
          <div className="space-y-6">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-5 w-1/4" />
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-12 w-48" />
          </div>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="container mx-auto px-6 lg:px-8 py-16 text-center">
        <p className="text-muted-foreground mb-4">Product not found.</p>
        <Link href="/">
          <Button variant="outline">Back to Shop</Button>
        </Link>
      </div>
    )
  }

  const tags = product.tags?.split(',').filter(Boolean) ?? []
  const inStock = (product.stock_quantity ?? 0) > 0

  return (
    <div className="min-h-screen">
      {/* Back button */}
      <div className="container mx-auto px-6 lg:px-8 pt-8">
        <button
          onClick={() => router.back()}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back
        </button>
      </div>

      {/* Main product section */}
      <div className="container mx-auto px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          {/* Image */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="relative aspect-square rounded-3xl overflow-hidden bg-muted/30"
          >
            {product.image_url ? (
              <Image
                src={product.image_url}
                alt={product.name}
                fill
                className="object-cover"
                priority
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <ShoppingBag className="h-24 w-24 text-muted-foreground/30" />
              </div>
            )}
          </motion.div>

          {/* Details */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-8"
          >
            {/* Category */}
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-widest">
              {product.category}
            </p>

            {/* Name */}
            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
              {product.name}
            </h1>

            {/* Rating placeholder */}
            <div className="flex items-center gap-2">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="h-4 w-4 fill-foreground text-foreground" />
              ))}
              <span className="text-sm text-muted-foreground ml-1">(42 reviews)</span>
            </div>

            {/* Price */}
            <div className="text-3xl font-semibold">
              ${product.price?.toFixed(2) ?? '0.00'}
            </div>

            {/* Description */}
            {product.description && (
              <p className="text-muted-foreground leading-relaxed text-base">
                {product.description}
              </p>
            )}

            {/* Tags */}
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {tags.map(tag => (
                  <span
                    key={tag}
                    className="px-3 py-1 text-xs rounded-full bg-muted text-muted-foreground"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Stock */}
            <p className={`text-sm font-medium ${inStock ? 'text-green-600 dark:text-green-400' : 'text-red-500'}`}>
              {inStock ? `In Stock (${product.stock_quantity} left)` : 'Out of Stock'}
            </p>

            {/* Actions */}
            <div className="flex gap-4 pt-2">
              <Button
                size="lg"
                className="flex-1 rounded-full py-6 text-base font-medium bg-foreground text-background hover:bg-foreground/90"
                onClick={handleAddToBag}
                disabled={!inStock}
              >
                <ShoppingBag className="mr-2 h-5 w-5" />
                {added ? 'Added!' : 'Add to Bag'}
              </Button>
              <Button
                size="icon"
                variant="outline"
                className="h-14 w-14 rounded-full"
              >
                <Heart className="h-5 w-5" />
              </Button>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Similar products */}
      {similar.length > 0 && (
        <div className="container mx-auto px-6 lg:px-8 py-16 border-t border-border/40">
          <h2 className="text-3xl font-bold tracking-tight mb-10">You May Also Like</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {similar.map((p, i) => (
              <motion.div
                key={p.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08, duration: 0.4 }}
              >
                <ProductCard product={p} />
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
