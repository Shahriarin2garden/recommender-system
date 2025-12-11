'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api-client'
import { BarChart, LineChart, TrendingUp, Users, ShoppingCart, Activity } from 'lucide-react'

interface ABTestMetrics {
  variant: string
  impressions: number
  clicks: number
  purchases: number
  ctr: number
  conversion_rate: number
}

interface ABTestResults {
  variants: ABTestMetrics[]
  winner: string | null
}

export default function AdminDashboard() {
  const [abTestResults, setAbTestResults] = useState<ABTestResults | null>(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(7)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await apiClient.getABTestResults(days)
        setAbTestResults(data as ABTestResults)
      } catch (error) {
        console.error('Failed to fetch A/B test results:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [days])

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
        <p className="text-muted-foreground">
          Monitor system performance and A/B test results
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
        <MetricCard
          title="Total Products"
          value="100"
          icon={<ShoppingCart className="h-4 w-4 text-muted-foreground" />}
          trend="+5%"
        />
        <MetricCard
          title="Active Users"
          value="50"
          icon={<Users className="h-4 w-4 text-muted-foreground" />}
          trend="+12%"
        />
        <MetricCard
          title="Avg API Latency"
          value="245ms"
          icon={<Activity className="h-4 w-4 text-muted-foreground" />}
          trend="-8%"
          trendPositive={true}
        />
        <MetricCard
          title="Recommendations"
          value="1,234"
          icon={<TrendingUp className="h-4 w-4 text-muted-foreground" />}
          trend="+24%"
        />
      </div>

      {/* A/B Test Results */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>A/B Test Results</CardTitle>
            <CardDescription>
              Last {days} days
              <select
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                className="ml-4 rounded border px-2 py-1"
              >
                <option value={7}>7 days</option>
                <option value={14}>14 days</option>
                <option value={30}>30 days</option>
              </select>
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div>Loading...</div>
            ) : abTestResults ? (
              <div className="space-y-4">
                {abTestResults.variants.map((variant) => (
                  <div
                    key={variant.variant}
                    className={`p-4 rounded-lg border ${
                      variant.variant === abTestResults.winner
                        ? 'border-primary bg-primary/5'
                        : 'border-border'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-semibold">
                        Variant {variant.variant}
                        {variant.variant === abTestResults.winner && (
                          <span className="ml-2 text-xs bg-primary text-primary-foreground px-2 py-1 rounded">
                            Winner
                          </span>
                        )}
                      </h3>
                      <div className="text-sm text-muted-foreground">
                        CTR: {variant.ctr.toFixed(2)}%
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <div className="text-muted-foreground">Impressions</div>
                        <div className="font-medium">{variant.impressions.toLocaleString()}</div>
                      </div>
                      <div>
                        <div className="text-muted-foreground">Clicks</div>
                        <div className="font-medium">{variant.clicks.toLocaleString()}</div>
                      </div>
                      <div>
                        <div className="text-muted-foreground">Purchases</div>
                        <div className="font-medium">{variant.purchases.toLocaleString()}</div>
                      </div>
                    </div>
                    <div className="mt-2">
                      <div className="flex justify-between text-xs text-muted-foreground mb-1">
                        <span>Click-through Rate</span>
                        <span>{variant.ctr.toFixed(2)}%</span>
                      </div>
                      <div className="h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary"
                          style={{ width: `${Math.min(variant.ctr * 10, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div>No data available</div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Performance Chart</CardTitle>
            <CardDescription>CTR comparison over time</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-muted-foreground">
              <div className="text-center">
                <BarChart className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>Chart visualization</p>
                <p className="text-sm">(Integrate Chart.js or Recharts)</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Latest user interactions and recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <ActivityItem
              action="Product View"
              user="User #12"
              product="Product #45"
              variant="A"
              time="2 minutes ago"
            />
            <ActivityItem
              action="Recommendation Click"
              user="User #8"
              product="Product #23"
              variant="B"
              time="5 minutes ago"
            />
            <ActivityItem
              action="Purchase"
              user="User #31"
              product="Product #67"
              variant="A"
              time="12 minutes ago"
            />
            <ActivityItem
              action="Product View"
              user="User #19"
              product="Product #12"
              variant="B"
              time="18 minutes ago"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function MetricCard({
  title,
  value,
  icon,
  trend,
  trendPositive = false,
}: {
  title: string
  value: string
  icon: React.ReactNode
  trend: string
  trendPositive?: boolean
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className={`text-xs ${trendPositive ? 'text-green-600' : 'text-muted-foreground'}`}>
          {trend} from last period
        </p>
      </CardContent>
    </Card>
  )
}

function ActivityItem({
  action,
  user,
  product,
  variant,
  time,
}: {
  action: string
  user: string
  product: string
  variant: string
  time: string
}) {
  return (
    <div className="flex items-center justify-between py-2 border-b last:border-0">
      <div className="flex-1">
        <div className="font-medium text-sm">{action}</div>
        <div className="text-xs text-muted-foreground">
          {user} • {product} • Variant {variant}
        </div>
      </div>
      <div className="text-xs text-muted-foreground">{time}</div>
    </div>
  )
}
