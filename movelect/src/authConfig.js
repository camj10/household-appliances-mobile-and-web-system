import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getCsrfToken } from './screens/getcsrftoken'; // Verifica la ruta

const createAxiosInstance = async () => {
  try {
    
    // Configura la instancia de Axios
    const axiosInstance = axios.create({
      baseURL: 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    axiosInstance.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('access_token');
        console.log("token de authConfig: ", token);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        console.log("config.headers después de interceptor: ", config.headers);
        return config;
      },
      (error) => Promise.reject(error)
    );

    return axiosInstance;
  } catch (error) {
    console.error('Error al configurar Axios:', error);
    throw error;
  }
};

export default createAxiosInstance;
