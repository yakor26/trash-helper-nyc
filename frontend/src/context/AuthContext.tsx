import  { createContext, useState, useContext, useEffect, useCallback } from "react";
import type { AuthProviderProps, Login, User, Register} from "../utils/helper";
import type { ReactNode } from "react"; 
import { api } from "../utils/api";
import { apiAuth } from "../utils/api";

export const AuthContext = createContext<AuthProviderProps>({
    user: null,
    token: "",
    login: () => {},
    logout: () => {}
})

export function AuthProvider({ children }: { children: ReactNode}) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string>(() => localStorage.getItem("access_token") || "");
    
    const logout = useCallback (() => {
        setUser(null);
        setToken("");
        localStorage.removeItem("access_token");
    }, []);

    useEffect(() => {
        const getUser = async () => {
        if (token) {
            try {
                const response = await apiAuth.get("/api/user/me");
                setUser(response.data)
            } catch (error) {
                logout();
        }  
    }}; 
    getUser();
}, [token, logout])
  
    const login = async (data: Login) => {
        const userParams = new URLSearchParams();
        userParams.append("username", data.username);
        userParams.append("password", data.password);
        const config = {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        }
        try {
            const response = await api.post("/api/auth/login", userParams, config)
            setToken(response.data.access_token);
            localStorage.setItem("access_token", response.data.access_token);
        } catch (error) {
            const msg = "Unable to login. Verify credentials and try again.";
            throw new Error(msg, {cause: error});
        }
        return;
    };

    const register = async (data: Register) => {
        try {
            const response = await api.post("/api/auth/register", data);
            setToken(response.data.access_token)
            localStorage.setItem("access_token", response.data.access_token);
        } catch (error) {
            console.log("Unable to register. Confirm meet validation requirements and try again.");
        }
        return;

    };


    return (
        <AuthContext.Provider value={{ user, token, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
    
}
export const useAuth = () => {
    return useContext(AuthContext);
}

