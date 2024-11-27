import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

const getAccessToken = () => localStorage.getItem('access_token');
const getRefreshToken = () => localStorage.getItem('refresh_token');

const setTokens = (accessToken: string, refreshToken?: string) => {
  localStorage.setItem('access_token', accessToken);
  if (refreshToken) {
    localStorage.setItem('refresh_token', refreshToken);
  }
};

const refreshToken = async () => {
  const refresh_token = getRefreshToken();
  if (!refresh_token) {
    throw new Error('Refresh token is not available.');
  }

  try {
    const config = attachAuthHeader({}, refresh_token);
    const response = await api.post('/auth/refresh', {}, config);
    const newAccessToken = response.data.access_token;
    const newRefreshToken = response.data.refresh_token;
    setTokens(newAccessToken, newRefreshToken);
    return newAccessToken;
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw error;
  }
};

const attachAuthHeader = (config: any = {}, token: string) => {
  if (!config.headers) {
    config.headers = {};
  }
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
};

export const fetchData = async (endpoint: string) => {
  let token = getAccessToken();

  if (!token) {
    throw new Error('Access token not available.');
  }

  try {
    const config = attachAuthHeader({}, token);
    const response = await api.get(endpoint, config);
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 401) {
      try {
        const refresh_token = await refreshToken();
        const config = attachAuthHeader({}, refresh_token);
        const response = await api.get(endpoint, config);
        return response.data;
      } catch (refreshError) {
        console.error('Error refreshing token:', refreshError);
        throw refreshError;
      }
    } else {
      console.error('Error fetching data:', error);
      throw error;
    }
  }
};

export const postData = async (endpoint: string, data: any) => {
  let token = getAccessToken();

  const requiresAuth = !['/login'].includes(endpoint);

  if (requiresAuth && !token) {
    throw new Error('Access token not available.');
  }

  try {
    let config = {};
    if (requiresAuth) {
      config = attachAuthHeader({}, token);
    }

    const response = await api.post(endpoint, data, config);
    return response.data;
  } catch (error: any) {
    if (requiresAuth && error.response && error.response.status === 401) {
      try {
        token = await refreshToken();
        const config = attachAuthHeader({}, token);
        const response = await api.post(endpoint, data, config);
        return response.data;
      } catch (refreshError) {
        console.error('Error refreshing token:', refreshError);
        throw refreshError;
      }
    } else {
      console.error('Error posting data:', error);
      throw error;
    }
  }
};
