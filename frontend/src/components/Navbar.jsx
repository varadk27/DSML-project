import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="text-xl font-bold text-gray-800">
            Resume Analyzer AI
          </div>
          <div className="flex items-center space-x-4">
            <a href="/" className="text-gray-600 hover:text-gray-800">Home</a>
            <a href="/about" className="text-gray-600 hover:text-gray-800">About</a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;