import axios from 'axios' ; 

const api = axios.create({
    baseURL: process.env.REACT ||'https://localhost:5000',
})