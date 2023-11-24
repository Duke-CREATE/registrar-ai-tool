// app/layout.tsx
import React, { ReactNode } from 'react';
import './styles/layout.css';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="layout">
      <header className="header">
        <h1 className="main-title">Duke Atlas</h1>
      </header>
      <main className="content">
        {children}
      </main>
      <footer className="footer">
        <p>&copy; 2023 Duke Atlas. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
