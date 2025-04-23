import { useState } from 'react'
import Navbar from '../components/Nav.jsx';
import Footer from '../components/Footer.jsx';
import Home from '../components/Home.jsx';

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
      <Home />
    </>
  )
}

export default App
