import { Routes, Route} from 'react-router-dom';
import React from 'react'
import Home from './pages/Home';
import Navbar from './components/navbar';
import StickyNavbar from './components/navbar';

function App(){
  return (
    <>
    <StickyNavbar />
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
    </>
  );
}

export default App