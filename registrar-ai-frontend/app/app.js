// _app.js (or _app.tsx if you are using TypeScript)
if (typeof window === 'undefined') {
  const fetch = require('node-fetch');
  global.Headers = global.Headers || fetch.Headers;
  global.Request = global.Request || fetch.Request;
  global.Response = global.Response || fetch.Response;
}

import React from 'react';
import Layout from './layout'; // Ensure the path to your Layout component is correct
import '../styles/globals.css'; // Ensure the path to your global styles is correct

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;
