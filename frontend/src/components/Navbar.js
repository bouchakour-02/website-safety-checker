import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={{ padding: '1rem', background: '#f5f5f5' }}>
      <Link to="/" style={{ marginRight: '1rem' }}>Home</Link>
      <Link to="/scan" style={{ marginRight: '1rem' }}>Scan URL</Link>
      <Link to="/login" style={{ marginRight: '1rem' }}>Login</Link>
      <Link to="/register">Register</Link>
    </nav>
  );
};

export default Navbar;
