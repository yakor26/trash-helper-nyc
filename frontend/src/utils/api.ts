import axios, { type AxiosInstance } from "axios";

export const api: AxiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 10000,
    headers: {"Content-Type": "application/json"}
});

export const apiAuth: AxiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 10000,
    headers: {"Content-Type": "application/json"},
    withCredentials: true
})
// request intereceptor
apiAuth.interceptors.request.use(
    (config) => {
        const accessToken = localStorage.getItem("access_token");
        config.headers.Authorization = `Bearer ${accessToken}`;
        return config;
    },
    (error) => {
        console.error("Request Interceptor Error:", error);
        return Promise.reject(error);
    }
)