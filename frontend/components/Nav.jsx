import { useState } from 'react';
import { Link } from 'wouter';
import logo from '../src/assets/logo.svg';

const scrollToSection = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

const Nav = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <header className="bg-[#121212] border-b border-gray-800 sticky top-0 z-10">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center">
          <div className="flex items-center">
            <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-bold">
              {/* <span className="text-xl">YT</span> */}
              <img src={logo} class="h-40 me-3" alt="YT Extractor" />
            </div>
            <h1 className="ml-2 text-xl font-bold text-white">YT Extractor</h1>
          </div>
        </div>
        
        <nav className="hidden md:flex space-x-6">
          <Link href="/" className="text-white border-b-2 border-primary font-medium">Home</Link>
          <button 
            onClick={() => scrollToSection('about')} 
            className="text-[#AAAAAA] hover:text-white transition duration-150"
          >
            About
          </button>
          <button 
            onClick={() => scrollToSection('footer')} 
            className="text-[#AAAAAA] hover:text-white transition duration-150"
          >
            Contact
          </button>
        </nav>
        
        <button className="md:hidden text-white" onClick={toggleMenu}>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
      
      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#1E1E1E] py-4">
          <div className="container mx-auto px-4 flex flex-col space-y-4">
            <Link href="/" className="text-white font-medium">Home</Link>
            <button 
              onClick={() => {
                scrollToSection('about');
                toggleMenu();
              }} 
              className="text-[#AAAAAA] hover:text-white transition duration-150 text-left"
            >
              About
            </button>
            <button 
              onClick={() => {
                scrollToSection('footer');
                toggleMenu();
              }} 
              className="text-[#AAAAAA] hover:text-white transition duration-150 text-left"
            >
              Contact
            </button>
          </div>
        </div>
      )}
    </header>
  );
};

export default Nav;