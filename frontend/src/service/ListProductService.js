// src/service/ListProductService.js


import axios from 'axios';

const API_URL = 'https://fakestoreapi.com/products';

export const ProductService = {
    async getProducts() {
        const response = await axios.get(API_URL);
        return response.data; // Directly returning the array of products
    }
};
