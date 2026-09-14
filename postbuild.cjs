const fs = require('fs');
const path = require('path');

const dist = path.join(__dirname, 'dist');
if (fs.existsSync(path.join(dist, 'index.html'))) {
  const indexHtml = fs.readFileSync(path.join(dist, 'index.html'), 'utf-8');
  
  // Create 404 fallback
  fs.writeFileSync(path.join(dist, '404.html'), indexHtml);
  
  // Create /runbook.html
  fs.writeFileSync(path.join(dist, 'runbook.html'), indexHtml);
  
  // Create /runbook/index.html
  fs.mkdirSync(path.join(dist, 'runbook'), { recursive: true });
  fs.writeFileSync(path.join(dist, 'runbook', 'index.html'), indexHtml);
  
  // Create Cloudflare Pages _redirects rule
  fs.writeFileSync(path.join(dist, '_redirects'), '/*  /index.html  200\n');
  
  console.log('Postbuild: Successfully generated 404.html, runbook.html, runbook/index.html, and _redirects');
}
