const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Monorepo: pin app root so Next does not pick the repo-level lockfile as the workspace root.
  turbopack: {
    root: path.join(__dirname),
  },
};

module.exports = nextConfig;