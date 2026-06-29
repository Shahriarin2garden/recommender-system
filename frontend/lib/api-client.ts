const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
const API_V1 = `${API_BASE_URL}/api/v1`;

export const apiClient = {
    getProducts: async () => {
        const response = await fetch(`${API_V1}/products/`);
        if (!response.ok) {
            throw new Error(`Failed to fetch products: ${response.statusText}`);
        }
        return response.json();
    },

    getProductById: async (id: number) => {
        const response = await fetch(`${API_V1}/products/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch product ${id}: ${response.statusText}`);
        }
        return response.json();
    },

    getRecommendations: async (userId: number) => {
        const response = await fetch(`${API_V1}/recommend/${userId}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch recommendations: ${response.statusText}`);
        }
        const data = await response.json();
        // Extract product objects from the recommendations array
        return data.recommendations?.map((r: any) => r.product) ?? [];
    },

    trackClick: async (userId: number, productId: number) => {
        const response = await fetch(
            `${API_V1}/track_click?user_id=${userId}&product_id=${productId}&interaction_type=click`,
            { method: 'POST' }
        );
        if (!response.ok) {
            console.error('Failed to track click', response.statusText);
        }
        return response.json();
    }
};
