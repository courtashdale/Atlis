// tools/add-path-header.js
const fs = require('fs');
const path = require('path');
const glob = require('glob');

const extensions = ['.js', '.jsx', '.ts', '.tsx', '.py'];
const commentMap = {
  '.js': '//',
  '.jsx': '//',
  '.ts': '//',
  '.tsx': '//',
  '.py': '#',
};

const files = glob.sync('**/*.{js,jsx,ts,tsx,py}', {
  ignore: ['node_modules/**', 'venv/**', 'dist/**', 'build/**'],
});

for (const file of files) {
  const stat = fs.statSync(file);
  if (stat.isDirectory()) continue;

  const ext = path.extname(file);
  const commentPrefix = commentMap[ext];
  if (!commentPrefix) continue;

  const content = fs.readFileSync(file, 'utf8');
  const relPath = path.relative(process.cwd(), file).replace(/\\/g, '/');
  const expectedHeader = `${commentPrefix} ${relPath}`;

  const lines = content.split('\n');

  // Case 1: File already has a comment on top
  if (lines[0].startsWith(commentPrefix)) {
    if (lines[0] !== expectedHeader) {
      // Update the outdated header
      lines[0] = expectedHeader;
      fs.writeFileSync(file, lines.join('\n'));
      console.log(`🔄 Updated header in ${relPath}`);
    } else {
      // Header is already correct
      continue;
    }
  } else {
    // Case 2: No header → insert it
    lines.unshift(expectedHeader);
    fs.writeFileSync(file, lines.join('\n'));
    console.log(`✔ Added header to ${relPath}`);
  }
}
