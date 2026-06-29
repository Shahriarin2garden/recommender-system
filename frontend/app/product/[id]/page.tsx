'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Image from 'next/image'
import { ShoppingBag, Heart, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { apiClient } from '@/lib/api-client'
import { addToCart } from '@/lib/cart'

interface Product {
  id: number
  name: string
  description?: string
  price: number
  category: string
  image_url?: string | null
  tags?: string
  stock_quantity?: number
}

export default function ProductPage() {
  const params = useParams()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isAdded, setIsAdded] = useState(false)

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await apiClient.getProduct(Number(params.id))
        setProduct(data as Product)
      } catch (err: any) {
        setError(err?.message || 'Failed to fetch product')
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchProduct()
    }
  }, [params.id])

  if (loading) {
    return (
      <div className="container mx-auto px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <Skeleton className="aspect-square w-full rounded-2xl" />
          <div className="space-y-6">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-6 w-1/2" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-12 w-40" />
          </div>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="container mx-auto px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <p className="text-muted-foreground">Product not found</p>
          <Link href="/">
            <Button variant="outline" className="mt-4">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  const handleAddToCart = () => {
    addToCart(product)
    setIsAdded(true)
    setTimeout(() => setIsAdded(false), 1400)
  }

  return (
    <div className="container mx-auto px-6 lg:px-8 py-8">
      <Link href="/">
        <Button variant="ghost" className="mb-6">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Products
        </Button>
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Product Image */}
        <div className="aspect-square overflow-hidden rounded-2xl bg-muted/30">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt={product.name}
              width={600}
              height={600}
              className="object-cover w-full h-full"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-muted/30">
              <ShoppingBag className="h-24 w-24 text-muted-foreground/30" />
            </div>
          )}
        </div>

        {/* Product Details */}
        <div className="space-y-6">
          <div>
            <p className="text-sm text-muted-foreground mb-2">{product.category}</p>
            <h1 className="text-3xl font-bold">{product.name}</h1>
          </div>

          <div className="text-2xl font-semibold">${product.price.toFixed(2)}</div>

          <div>
            <h3 className="font-semibold mb-2">Description</h3>
            <p className="text-muted-foreground">
              {product.description?.trim() || 'No description available for this product yet.'}
            </p>
          </div>

          {product.tags && (
            <div>
              <h3 className="font-semibold mb-2">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {product.tags.split(',').map((tag, index) => (
                  <span
                    key={`${product.id}-${tag.trim()}`}
                    className="px-3 py-1 bg-muted rounded-full text-sm"
                  >
                    {tag.trim()}
                  </span>
                ))}
              </div>
            </div>
          )}

          {product.stock_quantity !== undefined && (
            <div>
              <p className="text-sm text-muted-foreground">
                {product.stock_quantity > 0 
                  ? `${product.stock_quantity} in stock` 
                  : 'Out of stock'
                }
              </p>
            </div>
          )}

          <div className="flex gap-4">
            <Button 
              variant="glass"
              className="flex-1"
              disabled={product.stock_quantity === 0}
              onClick={handleAddToCart}
            >
              <ShoppingBag className="mr-2 h-4 w-4" />
              {isAdded ? 'Added to Cart' : 'Add to Cart'}
            </Button>
            <Button variant="glass" size="icon">
              <Heart className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}