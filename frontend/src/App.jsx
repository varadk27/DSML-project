import React from 'react';
import ResumeAnalyzer from './components/ResumeAnalyzer';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto py-8">
        <ResumeAnalyzer />
      </main>
    </div>
  );
}

export default App;