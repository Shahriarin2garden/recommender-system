import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  login: async (email: string, password: string) => {
    // backend expects OAuth2 Password Request Form (x-www-form-urlencoded)
    const formData = new URLSearchParams();
    formData.append('username', email); // backend uses 'username' for the email field
    formData.append('password', password);
    
    const response = await axiosInstance.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },

  logout: async () => {
    const response = await axiosInstance.post('/auth/logout');
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await axiosInstance.get('/auth/me');
    return response.data;
  },

  getProducts: async () => {
    const response = await axiosInstance.get('/products/');
    return response.data;
  },

  getProduct: async (id: number) => {
    const response = await axiosInstance.get(`/products/${id}`);
    return response.data;
  },

  getRecommendations: async (userId: number, top_n?: number) => {
    const response = await axiosInstance.get(`/recommend/${userId}`, {
      params: { top_n }
    });
    return response.data;
  },

  getSimilarProducts: async (productId: number, top_n?: number) => {
    const response = await axiosInstance.get(`/similar/${productId}`, {
      params: { top_n }
    });
    return response.data;
  },

  trackClick: async (payload: { user_id: number; product_id: number; interaction_type?: string }) => {
    const response = await axiosInstance.post('/track_click', payload);
    return response.data;
  },

  getABTestResults: async (days?: number) => {
    const response = await axiosInstance.get('/ab-test/results', {
      params: { days }
    });
    return response.data;
  }
};
