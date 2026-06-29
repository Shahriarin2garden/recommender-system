'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ProductCard } from '@/components/product-card'
import { Skeleton } from '@/components/ui/skeleton'
import { apiClient } from '@/lib/api-client'

interface Product {
    id: number
    name: string
    price?: number
    category: string
    image_url?: string | null
}

export function RecommendationSection({ userId }: { userId: number }) {
    const [products, setProducts] = useState<Product[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const data = await apiClient.getRecommendations(userId)
                setProducts(data as Product[])
            } catch (err: any) {
                console.error('Failed to fetch recommendations:', err)
            } finally {
                setLoading(false)
            }
        }

        fetchRecommendations()
    }, [userId])

    if (loading) {
        return (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {[...Array(4)].map((_, i) => (
                    <div key={i} className="space-y-4">
                        <Skeleton className="h-64 w-full rounded-2xl" />
                        <Skeleton className="h-4 w-3/4" />
                        <Skeleton className="h-4 w-1/2" />
                    </div>
                ))}
            </div>
        )
    }

    if (products.length === 0) {
        return null;
    }

    return (
        <>
            <h2 className="mb-10 text-4xl sm:text-5xl font-bold tracking-tight">Recommended for You</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {products.map((product, index) => (
                    <motion.div
                        key={product.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1, duration: 0.5 }}
                    >
                        <ProductCard product={product} />
                    </motion.div>
                ))}
            </div>
        </>
    )
}
