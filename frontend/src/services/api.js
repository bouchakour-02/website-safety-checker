import axios from 'axios' ; 

const api = axios.create({
    baseURL: process.env.REACT_APP ||'https://localhost:5000',
})