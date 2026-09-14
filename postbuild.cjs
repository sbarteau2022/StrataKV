const fs = require('fs');
const path = require('path');

const dist = path.join(__dirname, 'dist');
if (fs.existsSync(path.join(dist, 'index.html'))) {
  const indexHtml = fs.readFileSync(path.join(dist, 'index.html'), 'utf-8');
  
  // Create 404 fallback for static hosts
  fs.writeFileSync(path.join(dist, '404.html'), indexHtml);
  
  // Create /runbook.html for static direct file serving
  fs.writeFileSync(path.join(dist, 'runbook.html'), indexHtml);
  
  // Create /runbook/index.html for static directory serving
  fs.mkdirSync(path.join(dist, 'runbook'), { recursive: true });
  fs.writeFileSync(path.join(dist, 'runbook', 'index.html'), indexHtml);
  
  console.log('Postbuild: Successfully generated 404.html, runbook.html, and runbook/index.html');
}
