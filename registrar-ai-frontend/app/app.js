// _app.js (or _app.tsx if you are using TypeScript)
import React from 'react';
import Layout from './layout'; // Adjust the import path based on your project structure
import '../styles/globals.css'; // Global styles, adjust path as necessary

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;