const http = require('http');
const fs = require('fs');
const path = require('path');
const accessLog = require('../access-logger')('treehouse-public');
const ROOT = __dirname;

const MIME = {'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.gif':'image/gif','.svg':'image/svg+xml','.ico':'image/x-icon'};

const server = http.createServer((req, res) => {
  accessLog(req);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if(req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  if(req.method === 'POST' && req.url === '/save-img') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const {name, data} = JSON.parse(body);
        const safeName = name.replace(/[^a-zA-Z0-9_.-]/g, '');
        fs.writeFileSync(path.join(ROOT, 'img', safeName), Buffer.from(data, 'base64'));
        res.writeHead(200, {'Content-Type':'application/json'});
        res.end(JSON.stringify({ok:true, name: safeName}));
      } catch(e) { res.writeHead(500); res.end(e.message); }
    });
    return;
  }

  let fp = path.join(ROOT, req.url === '/' ? 'index.html' : decodeURIComponent(req.url));
  if(!fs.existsSync(fp)) { res.writeHead(404); res.end('Not found'); return; }
  const ext = path.extname(fp);
  res.writeHead(200, {'Content-Type': MIME[ext] || 'application/octet-stream'});
  fs.createReadStream(fp).pipe(res);
});

server.listen(3007, '127.0.0.1', () => console.log('Treehouse public on :3007'));
