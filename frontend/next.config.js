const path = require('path');

/** App directory (this file lives in frontend/) */
const appRoot = __dirname;

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Next may set outputFileTracingRoot; turbopack.root must match to avoid the build warning.
  outputFileTracingRoot: appRoot,
  turbopack: {
    root: appRoot,
  },
};

module.exports = nextConfig;