'use client'

import { useEffect, useState } from 'react'
import { Sparkles } from 'lucide-react'
import { ProductCard } from '@/components/product-card'
import { apiClient } from '@/lib/api-client'
import { Skeleton } from '@/components/ui/skeleton'

interface Recommendation {
  product_id: number
  score: number
  rank: number
  product: {
    id: number
    name: string
    description?: string
    price: number
    category: string
    image_url?: string | null
    tags?: string
  }
}

interface RecommendationsResponse {
  user_id: number
  recommendations: Recommendation[]
  model_version: string
  generated_at?: string
}

export function RecommendationSection({ userId }: { userId: number }) {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [modelVersion, setModelVersion] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const data = (await apiClient.getRecommendations(userId, 4)) as RecommendationsResponse
        setRecommendations(data.recommendations || [])
        setModelVersion(data.model_version || '')
      } catch (err: any) {
        console.error('Failed to fetch recommendations:', err)
        setError(err?.message || 'Failed to load recommendations')
      } finally {
        setLoading(false)
      }
    }

    if (userId) {
      fetchRecommendations()
    }
  }, [userId])

  if (loading) {
    return (
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div className="h-8 w-52 skeleton" />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="space-y-3">
              <div className="aspect-square w-full skeleton rounded-2xl" />
              <div className="h-4 w-3/4 skeleton" />
              <div className="h-3 w-1/2 skeleton" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (error || recommendations.length === 0) {
    return null // Gracefully hide the section if backend fails or has no recommendations
  }

  return (
    <div className="space-y-12 animate-fade-in">
      <div className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <p className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-3 flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5 text-foreground animate-pulse-dot" />
            AI-Engine
          </p>
          <h2 className="text-4xl sm:text-5xl font-bold tracking-tight">Picks For You</h2>
        </div>
        {modelVersion && (
          <span className="text-[10px] tracking-[0.2em] uppercase text-muted-foreground/60 border border-border/60 bg-muted/40 px-3 py-1 rounded-full font-medium">
            Model: {modelVersion}
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {recommendations.map((rec) => (
          <div key={rec.product_id} className="relative group">
            <ProductCard product={rec.product} />
            {rec.score && (
              <span className="absolute top-3 left-3 z-10 text-[10px] bg-background/90 backdrop-blur-sm border border-border/40 font-semibold px-2 py-0.5 rounded-full pointer-events-none tabular-nums opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                Match: {Math.round(rec.score * 100)}%
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
