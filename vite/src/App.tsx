import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import {  useLocation, Routes,Route} from "react-router-dom";
import Home from './pages/Home';
import CarDetails from './pages/CarDetails';
import Cars from './pages/Cars';
import Bookings from './pages/Bookings';
import Footer from './components/Footer';

function App() {
  const [showLogin,setShowLogin]=useState(false)
  const isOwnerPath=useLocation().pathname.startsWith('/owner')
  return (
    <>
      {!isOwnerPath && <Navbar setShowLogin={setShowLogin}/>}
      {/* page routes */}
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/car-details/:id' element={<CarDetails/>}/>
        <Route path='/cars' element={<Cars/>}/>
        <Route path='/bookings' element={<Bookings/>}/>
        <Route path='/' element={<Home/>}/>
      </Routes>
      {!isOwnerPath && <Footer/>}
      
    </>
  )
}

export default App
