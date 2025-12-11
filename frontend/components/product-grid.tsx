'use client'

import { useEffect, useState } from 'react'
import { ProductCard } from './product-card'
import { Skeleton } from './ui/skeleton'
import { apiClient } from '@/lib/api-client'

interface Product {
  id: number
  name: string
  price?: number
  category: string
  image_url?: string | null
}

export function ProductGrid() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProducts = async () => {
      const timeout = setTimeout(() => {
        setError('Request timed out. Backend may be down or endpoint is incorrect.')
        setLoading(false)
      }, 10000) // 10 seconds
      try {
        const data = await apiClient.getProducts()
        setProducts(data as Product[])
      } catch (err: any) {
        setError(err?.message || 'Failed to fetch products')
        console.error('Failed to fetch products:', err)
      } finally {
        clearTimeout(timeout)
        setLoading(false)
      }
    }

    fetchProducts()
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="space-y-4">
            <Skeleton className="aspect-square w-full rounded-2xl" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Unable to load products at this time.</p>
        <p className="text-sm text-muted-foreground/60 mt-2">Please try again later.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      {products.map((product) => (
        <div key={product.id} className="animate-fade-in">
          <ProductCard product={product} />
        </div>
      ))}
    </div>
  )
}
