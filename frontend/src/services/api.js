import axios from 'axios' ; 

const api = axios.create({
    baseURL: ProcessingInstruction.env ||'https://localhost:5000',
})