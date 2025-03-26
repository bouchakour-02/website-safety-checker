import axios from 'axios' ; 

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL ||'https://localhost:5000',
});

api.interceptors.request.use((config)=>{}
const token = localStorage.getItem('access_token');
if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
}
return config ;
)