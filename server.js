const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8080;
const baseUrl = `http://localhost:${PORT}`;
const courseData = JSON.parse(fs.readFileSync('./static/course_data.json', 'utf8'));

const MIME = {
    '.html': 'text/html',
    '.json': 'application/json',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.mp3': 'audio/mpeg'
};

const server = http.createServer((req, res) => {
    if (req.url.startsWith('/api/audio')) {
        const url = new URL(req.url, baseUrl);
        const text = url.searchParams.get('text') || '';
        
        if (!text) {
            res.writeHead(400, {'Content-Type': 'application/json'});
            res.end(JSON.stringify({ error: 'Text is required' }));
            return;
        }
        
        const encodedText = encodeURIComponent(text);
        const ttsUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q=${encodedText}`;
        
        https.get(ttsUrl, (proxyRes) => {
            if (proxyRes.statusCode !== 200) {
                res.writeHead(proxyRes.statusCode, {'Content-Type': 'application/json'});
                res.end(JSON.stringify({ error: 'TTS request failed' }));
                return;
            }
            
            res.writeHead(200, {'Content-Type': 'audio/mpeg', 'Access-Control-Allow-Origin': '*'});
            proxyRes.pipe(res);
        }).on('error', (e) => {
            console.error('TTS error:', e.message);
            res.writeHead(500, {'Content-Type': 'application/json'});
            res.end(JSON.stringify({ error: e.message }));
        });
        return;
    }
    
    if (req.url === '/api/course') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({ modules: courseData.modules.map(m => ({
            ...m,
            word_count: m.lessons.reduce((sum, l) => sum + (l.words?.length || 0), 0)
        }))}));
        return;
    }
    
    let filePath = path.join(__dirname, 'static', req.url === '/' ? 'index.html' : req.url);
    
    if (!fs.existsSync(filePath)) {
        filePath = path.join(__dirname, 'static', 'index.html');
    }
    
    const ext = path.extname(filePath);
    const contentType = MIME[ext] || 'text/plain';
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found');
            return;
        }
        res.writeHead(200, {'Content-Type': contentType});
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});