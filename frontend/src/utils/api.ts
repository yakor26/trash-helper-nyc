import axios, { type AxiosInstance } from "axios";

export const api: AxiosInstance = axios.create({
    baseURL: "https://trashhelper-369898338593.us-east1.run.app",
    headers: {"Content-Type": "application/json"}
});

export const apiAuth: AxiosInstance = axios.create({
    baseURL: "https://trashhelper-369898338593.us-east1.run.app",
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


