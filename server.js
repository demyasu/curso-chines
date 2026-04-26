const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 9090;
const baseUrl = `http://localhost:${PORT}`;

let courseData;
try {
    courseData = JSON.parse(fs.readFileSync('./course_data.json', 'utf8'));
} catch (e) {
    courseData = JSON.parse(fs.readFileSync('./static/course_data.json', 'utf8'));
}

const MIME = {
    '.html': 'text/html',
    '.json': 'application/json',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.mp3': 'audio/mpeg'
};

const server = http.createServer((req, res) => {
    // TTS API
    if (req.url.startsWith('/api/tts')) {
        const url = new URL(req.url, baseUrl);
        const text = url.searchParams.get('text') || '';
        
        if (!text) {
            res.writeHead(400, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'});
            res.end(JSON.stringify({ error: 'Text is required' }));
            return;
        }
        
        const encodedText = encodeURIComponent(text);
        const ttsUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q=${encodedText}`;
        
        https.get(ttsUrl, (proxyRes) => {
            if (proxyRes.statusCode !== 200) {
                res.writeHead(proxyRes.statusCode, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'});
                res.end(JSON.stringify({ error: 'TTS failed: ' + proxyRes.statusCode }));
                return;
            }
            
            res.writeHead(200, {
                'Content-Type': 'audio/mpeg',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            });
            proxyRes.pipe(res);
        }).on('error', (e) => {
            console.error('TTS error:', e.message);
            res.writeHead(500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'});
            res.end(JSON.stringify({ error: e.message }));
        });
        return;
    }
    
    // Course API
    if (req.url === '/api/course') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({ modules: courseData.modules.map(m => ({
            ...m,
            word_count: m.lessons.reduce((sum, l) => sum + (l.words?.length || 0), 0)
        }))}));
        return;
    }
    
    // CORS headers for API
    if (req.url.startsWith('/api/')) {
        res.writeHead(200, {'Access-Control-Allow-Origin': '*'});
        res.end();
        return;
    }
    
    // Static files
    let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    
    // Try static folder first
    if (!fs.existsSync(filePath)) {
        filePath = path.join(__dirname, 'static', req.url === '/' ? 'index.html' : req.url);
    }
    
    // Fallback to index.html
    if (!fs.existsSync(filePath)) {
        filePath = path.join(__dirname, 'index.html');
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