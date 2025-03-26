import axios from 'axios' ; 

const api = axios.create({
    baseURL: process ||'https://localhost:5000',
})