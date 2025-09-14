
// src/service/AuthService.js

import axios from 'axios';

// Define the base URL for your API
// const API_URL = 'https://crucial-gerrilee-hour-cadf9ee0.koyeb.app/v1/auth/admin/api/';
const API_URL = 'http://127.0.0.1:8000/v1/auth/admin/api/';

// Create an Axios instance with the base URL
const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});


export const login = async (email, password) => {
    try {
        const response = await apiClient.post('login', { email, password });

        // Ensure to return the necessary data based on your API response
        if (response.data.status === 200) {
            return {
                success: true,
                accessToken: response.data.data.jwt.access_token,
                refreshToken: response.data.data.refresh_token,
                message: response.data.message,
            };
        } else {
            return { success: false, message: response.data.message };
        }
    } catch (error) {
        // Log the error response if available
        console.error('Login failed:', error.response ? error.response.data : error.message);
        // Return a structured error response
        return {
            success: false,
            message: error.response?.data?.detail || 'An unexpected error occurred. Please try again.'
        };
    }
};

export const logout = async (token) => {
    try {
        await apiClient.post('logout', {}, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });
    } catch (error) {
        console.error('Logout API call failed:', error.response ? error.response.data : error.message);
    }
};
