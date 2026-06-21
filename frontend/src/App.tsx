import { useState } from 'react'
import Navbar from './components/Navbar'
import MainSection from './components/MainSection'
import ScheduleSidebar from './components/ScheduleSidebar'
import StatusSidebar from './components/StatusSidebar'
import { Outlet } from 'react-router'
import { Box } from "@chakra-ui/react"


function App() {
  return (
    <>
    <Navbar/>
    <Outlet/> 
    </>
  )
}

export default App
