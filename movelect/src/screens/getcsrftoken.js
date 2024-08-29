import axios from 'axios';

export const getCsrfToken = async () => {
    try {
        const response = await axios.get('http://localhost:8000/csrf-token/', { withCredentials: true });
        console.log("response.data.csrfToken: ",response.data.csrfToken);
        return response.data.csrfToken;
    } catch (error) {
        console.error('Error al obtener el CSRF token:', error);
        throw error;
    }
};