import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8006',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: async (formData: any) => {
    const params = new URLSearchParams();
    params.append('username', formData.email);
    params.append('password', formData.password);
    const response = await api.post('/auth/access-token', params);
    return response.data;
  },
  register: async (userData: any) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },
  me: async () => {
    const response = await api.get('/users/me');
    return response.data;
  }
};

export const invoices = {
  list: async () => {
    const response = await api.get('/invoices/');
    return response.data;
  },
  get: async (id: string) => {
    const response = await api.get(`/invoices/${id}`);
    return response.data;
  },
  create: async (invoice: any) => {
    const response = await api.post('/invoices/', invoice);
    return response.data;
  },
  update: async (id: string, invoice: any) => {
    const response = await api.put(`/invoices/${id}`, invoice);
    return response.data;
  },
  delete: async (id: string) => {
    const response = await api.delete(`/invoices/${id}`);
    return response.data;
  },
  getPdfUrl: (id: string) => {
    return `${api.defaults.baseURL}/invoices/${id}/pdf`;
  }
};

export default api;
