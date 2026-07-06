import { useAuth } from "../context/AuthContext";
import { Outlet, Navigate, useLocation } from "react-router";
export const ProtectedRoute = () => {
    const { token } = useAuth();
    const location = useLocation();
    if (!token) {
        return <Navigate to={"/login"} replace state={{from: location}}/>
    }
    return <Outlet/>
}