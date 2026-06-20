import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
// import './App.css'
import Navbar from './components/Navbar'
import { Outlet } from 'react-router'


function App() {
  return (
    <>
    <Navbar/>
    <h1>Temporary Home</h1>
    <Outlet/>
    </>
  )
}

export default App
