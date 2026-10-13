const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

function buildApiUrl(path: string) {
  const endpoint = path.startsWith('/') ? path : `/${path}`;

  if (API_BASE.startsWith('http://') || API_BASE.startsWith('https://')) {
    const base = API_BASE.endsWith('/api') ? API_BASE : `${API_BASE}/api`;
    return new URL(`${base}${endpoint}`, window.location.origin).toString();
  }

  return new URL(`${API_BASE}${endpoint}`, window.location.origin).toString();
}

export const apiClient = {
  getProducts: async () => {
    const response = await fetch(buildApiUrl('/v1/products/'), {
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }
    return response.json();
  },

  getProduct: async (id: number) => {
    const response = await fetch(buildApiUrl(`/v1/products/${id}`), {
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch product ${id}: ${response.statusText}`);
    }
    return response.json();
  },

  getProductById: async (id: number) => {
    return apiClient.getProduct(id);
  },

  getCurrentUser: async () => {
    const response = await fetch(buildApiUrl('/v1/auth/me'), {
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch current user: ${response.statusText}`);
    }
    return response.json();
  },

  login: async (email: string, password: string) => {
    const response = await fetch(buildApiUrl('/v1/auth/login'), {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: email,
        password,
      }).toString(),
    });

    if (!response.ok) {
      const detail = await response.json().catch(() => ({}));
      throw new Error(detail?.detail || `Login failed: ${response.statusText}`);
    }
    return response.json();
  },

  logout: async () => {
    const response = await fetch(buildApiUrl('/v1/auth/logout'), {
      method: 'POST',
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Logout failed: ${response.statusText}`);
    }
    return response.json();
  },

  getRecommendations: async (userId: number, limit = 10) => {
    const response = await fetch(buildApiUrl(`/v1/recommend/${userId}?top_n=${limit}`), {
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch recommendations: ${response.statusText}`);
    }
    return response.json();
  },

  getABTestResults: async (days = 7) => {
    const response = await fetch(buildApiUrl(`/v1/ab-test/results?days=${days}`), {
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch A/B test results: ${response.statusText}`);
    }
    return response.json();
  },

  trackClick: async (userId: number, productId: number) => {
    const response = await fetch(buildApiUrl(`/v1/track_click?user_id=${userId}&product_id=${productId}&interaction_type=click`), {
      method: 'POST',
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error(`Failed to track click: ${response.statusText}`);
    }
    return response.json();
  },
};
