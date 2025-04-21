import { Routes, Route} from 'react-router-dom';
import React from 'react'
import Home from './pages/Home';
import Navbar from './components/navbar';

function App(){
  return (
    <>
    <Navbar />
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
    </>
  );
}

export default App