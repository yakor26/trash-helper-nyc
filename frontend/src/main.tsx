import { ChakraProvider } from '@chakra-ui/react'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from "react-router"
import '@fontsource-variable/open-sans/wght.css'
import '@fontsource-variable/outfit/wght.css'
import App from './App.tsx'
import SearchPage from "./pages/SearchPage.tsx"
import SchedulePage from "./pages/SchedulePage.tsx"
import LoginPage from "./pages/LoginPage.tsx"
import RegisterPage from "./pages/RegisterPage.tsx"
import HomePage from "./pages/HomePage.tsx"
import UserProfilePage from './pages/UserProfilePage.tsx'
import { ProtectedRoute } from './components/ProtectedRoute.tsx'
import { RestrictedProtectedRoute } from './components/RestrictedPublicRoute.tsx'
import theme from "./utils/theme.ts"
import { AuthProvider } from './context/AuthContext.tsx'
const router = createBrowserRouter([
  {
    path: "/",
    Component: App,
    children: [
      {index: true, Component: HomePage},
      {path: "search", Component: SearchPage},
      {Component: RestrictedProtectedRoute,
        children: [
          {path: "login", Component: LoginPage},
          {path: "register", Component: RegisterPage},
        ]
       },
      
      {Component: ProtectedRoute,
        children: [
          {path: "schedule", Component: SchedulePage},
          {path: "profile", Component: UserProfilePage}
        ]
      },
      {path: "*", element: <Navigate to={"/"} replace />}
    ]
  }
]
)
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChakraProvider theme={theme}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </ChakraProvider>
  </StrictMode>
)
