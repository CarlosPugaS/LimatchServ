import { Routes, Route} from 'react-router-dom';
import React from 'react'
import Home from './pages/Home';
import StickyNavbar from './components/navbar';
import Hero from './components/hero';
import Footer from './components/footer'

function App(){
  return (
    <div className='flex flex-col min-h-screen'>
    <StickyNavbar />
    <main className='flex flex-grow'> 
    <Hero />
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
    </main>
    <Footer />
    </div>
  );
}

export default App