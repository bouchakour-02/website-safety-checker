import axios from 'axios' ; 

const api = axios.create({
    baseURL: process.env ||'https://localhost:5000',
})