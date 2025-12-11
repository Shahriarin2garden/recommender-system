'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ProductCard } from './product-card'
import { Skeleton } from './ui/skeleton'
import { apiClient } from '@/lib/api-client'

interface Product {
  id: number
  name: string
  price: number
  category: string
  image_url: string
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
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="space-y-4">
            <Skeleton className="h-64 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-red-600 p-4 text-center">
        Error loading products: {error}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {products.map((product, index) => (
        <motion.div
          key={product.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
        >
          <ProductCard product={product} />
        </motion.div>
      ))}
    </div>
  )
}
