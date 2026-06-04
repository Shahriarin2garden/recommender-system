'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { User, Activity, Sparkles, LogOut, ArrowRight, UserCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api-client'
import { Skeleton } from '@/components/ui/skeleton'
import axios from 'axios'

interface UserProfile {
  id: number
  email: string
  full_name?: string
  is_active: boolean
  cohort?: string
}

export default function UserDashboard() {
  const router = useRouter()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [cohortInfo, setCohortInfo] = useState<{ cohort: string; variant: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [assigningCohort, setAssigningCohort] = useState(false)

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const user = await apiClient.getCurrentUser()
        setProfile(user)
        
        // Fetch cohort variant info
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const cohortRes = await axios.get(`${API_BASE_URL}/api/v1/ab-test/user-cohort/${user.id}`, {
          withCredentials: true
        })
        setCohortInfo(cohortRes.data)
      } catch (err: any) {
        console.error('Not logged in or error:', err)
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }

    fetchUserData()
  }, [router])

  const handleLogout = async () => {
    try {
      await apiClient.logout()
      router.push('/login')
      router.refresh()
    } catch (err) {
      console.error('Logout failed:', err)
    }
  }

  const handleAssignCohort = async (variant: string) => {
    if (!profile) return
    setAssigningCohort(true)
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await axios.post(`${API_BASE_URL}/api/v1/ab-test/assign-cohort/${profile.id}?cohort=${variant}`, {}, {
        withCredentials: true
      })
      setCohortInfo({ cohort: variant, variant })
    } catch (err) {
      console.error('Failed to assign cohort:', err)
    } finally {
      setAssigningCohort(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-6 lg:px-8 py-12 space-y-8">
        <Skeleton className="h-10 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Skeleton className="h-40 rounded-2xl" />
          <Skeleton className="h-40 rounded-2xl" />
          <Skeleton className="h-40 rounded-2xl" />
        </div>
      </div>
    )
  }

  if (!profile) return null

  return (
    <div className="container mx-auto px-6 lg:px-8 py-12 animate-fade-in space-y-12">
      
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4 border-b border-border/55 pb-6">
        <div>
          <h1 className="text-4xl font-bold tracking-tight">Account Dashboard</h1>
          <p className="text-muted-foreground text-sm mt-1">Manage your profile and A/B cohort settings</p>
        </div>
        <Button variant="ghost" className="hover:bg-destructive/10 hover:text-destructive transition-colors duration-200" onClick={handleLogout}>
          <LogOut className="h-4 w-4 mr-2" />
          Sign Out
        </Button>
      </div>

      {/* Grid overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Profile Details Card */}
        <Card className="shadow-none rounded-2xl border border-border/60">
          <CardHeader className="flex flex-row items-center gap-4 pb-2">
            <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center border border-border/60">
              <User className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg">Profile Details</CardTitle>
              <CardDescription>Logged in credentials</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-4 space-y-2 text-sm">
            <div>
              <span className="text-muted-foreground block text-xs uppercase tracking-wider">Email</span>
              <span className="font-medium text-foreground">{profile.email}</span>
            </div>
            <div>
              <span className="text-muted-foreground block text-xs uppercase tracking-wider">User ID</span>
              <span className="font-mono text-xs font-medium text-foreground">#{profile.id}</span>
            </div>
          </CardContent>
        </Card>

        {/* Recommender Cohort Card */}
        <Card className="shadow-none rounded-2xl border border-border/60">
          <CardHeader className="flex flex-row items-center gap-4 pb-2">
            <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center border border-border/60">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg">Recommendation Cohort</CardTitle>
              <CardDescription>A/B test variant assignment</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-4 space-y-4">
            <div>
              <span className="text-muted-foreground block text-xs uppercase tracking-wider mb-1">Active Variant</span>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-bold tracking-tight">
                  Variant {cohortInfo?.cohort || 'Unknown'}
                </span>
                <span className="text-[10px] bg-green-500/10 text-green-500 border border-green-500/20 px-2 py-0.5 rounded-full font-medium">
                  Active
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Change Cohort Card for Developers/Demo */}
        <Card className="shadow-none rounded-2xl border border-border/60">
          <CardHeader className="flex flex-row items-center gap-4 pb-2">
            <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center border border-border/60">
              <UserCheck className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg">Cohort Simulator</CardTitle>
              <CardDescription>Swap cohorts to test algorithms</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-4 space-y-3">
            <p className="text-xs text-muted-foreground leading-relaxed">
              Manually assign yourself to a variant to see how the recommendations algorithm changes.
            </p>
            <div className="flex gap-2">
              <Button 
                variant={cohortInfo?.cohort === 'A' ? 'default' : 'outline'}
                size="sm" 
                className="flex-1 rounded-full h-8"
                disabled={assigningCohort}
                onClick={() => handleAssignCohort('A')}
              >
                Variant A
              </Button>
              <Button 
                variant={cohortInfo?.cohort === 'B' ? 'default' : 'outline'}
                size="sm" 
                className="flex-1 rounded-full h-8"
                disabled={assigningCohort}
                onClick={() => handleAssignCohort('B')}
              >
                Variant B
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Activity Details section */}
      <Card className="shadow-none rounded-2xl border border-border/60">
        <CardHeader className="flex flex-row items-center gap-4 pb-2 border-b border-border/55">
          <div className="h-10 w-10 rounded-full bg-primary/5 flex items-center justify-center border border-border/60">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <CardTitle className="text-lg">Recent Interactions</CardTitle>
            <CardDescription>Activity logs stored for your personalization model</CardDescription>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-border/40 text-sm">
            <div className="p-4 flex items-center justify-between hover:bg-muted/10 transition-colors">
              <div>
                <p className="font-medium text-foreground">Viewed Product ID #15</p>
                <p className="text-xs text-muted-foreground mt-0.5">Personalized recommendation feed item</p>
              </div>
              <span className="text-xs text-muted-foreground">Just now</span>
            </div>
            <div className="p-4 flex items-center justify-between hover:bg-muted/10 transition-colors">
              <div>
                <p className="font-medium text-foreground">Added Product ID #4 to Cart</p>
                <p className="text-xs text-muted-foreground mt-0.5">Interaction tracked in Cohort {cohortInfo?.cohort || 'A'}</p>
              </div>
              <span className="text-xs text-muted-foreground">5 minutes ago</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
