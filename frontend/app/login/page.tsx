'use client'

import { FormEvent, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api-client'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('alice@example.com')
  const [password, setPassword] = useState('password123')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const token = await apiClient.login(email, password)
      localStorage.setItem('recommender_token', token.access_token)

      const user = await apiClient.getCurrentUser(token.access_token)
      localStorage.setItem('recommender_user', JSON.stringify(user))

      router.push('/')
      router.refresh()
    } catch (err: any) {
      setError(err?.message || 'Login failed. Please verify your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-6 lg:px-8 py-10 flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Sign in</CardTitle>
          <CardDescription>Use a seeded account to continue.</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">Email</label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">Password</label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              />
            </div>

            {error && <p className="text-sm text-destructive">{error}</p>}

            <Button className="w-full" type="submit" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>

          <div className="mt-4 text-sm text-muted-foreground">
            <p>Demo account:</p>
            <p>alice@example.com / password123</p>
          </div>

          <div className="mt-4 text-sm">
            <Link href="/" className="underline underline-offset-4">
              Back to home
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
