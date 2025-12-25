import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import {  useLocation, Routes,Route} from "react-router-dom";
import Home from './pages/Home';
import CarDetails from './pages/CarDetails';
import Cars from './pages/Cars';
import Bookings from './pages/Bookings';
import Footer from './components/Footer';
import Layout from './pages/owner/Layout';
import Dashboard from './pages/owner/Dashboard';
import AddCar from './pages/owner/AddCar';
import ManageCars from './pages/owner/ManageCars';
import ManageBookings from './pages/owner/ManageBookings';

function App() {
  const [showLogin,setShowLogin]=useState(false)
  const isOwnerPath=useLocation().pathname.startsWith('/owner')
  return (
    <>
      {!isOwnerPath && <Navbar setShowLogin={setShowLogin}/>}
      {/* page routes */}
      <Routes>
        {/* routes for normal user */}
        <Route path='/' element={<Home/>}/>
        <Route path='/car-details/:id' element={<CarDetails/>}/>
        <Route path='/cars' element={<Cars/>}/>
        <Route path='/my-bookings' element={<Bookings/>}/>
        <Route path='/' element={<Home/>}/> 
        {/* routes for owner */}
        <Route path='/owner' element={<Layout/>}> 
        <Route index element={<Dashboard/>}/> 
        <Route path="add-car" element={<AddCar/>}/> 
        <Route path="manage-cars" element={<ManageCars/>}/> 
        <Route path="manage-bookings" element={<ManageBookings/>}/> 
        </Route>
      </Routes>
      {!isOwnerPath && <Footer/>}
      
    </>
  )
}

export default App
