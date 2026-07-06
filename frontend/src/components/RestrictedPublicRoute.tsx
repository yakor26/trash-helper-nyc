import { useAuth } from "../context/AuthContext";
import { Outlet, Navigate } from "react-router";
export const RestrictedProtectedRoute = () => {
    const { token } = useAuth();
    if (token) {
        return <Navigate to={"/search"}/>
    }
    return <Outlet/>
}