const https = require('https');

module.exports = (req, res) => {
    const text = req.query.text || (req.body && req.body.text);
    const lang = req.query.lang || 'zh-CN';
    
    if (!text) {
        return res.status(400).json({ error: 'Text is required' });
    }
    
    const encodedText = encodeURIComponent(text);
    const ttsUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${lang}&client=tw-ob&q=${encodedText}`;
    
    const request = https.get(ttsUrl, (proxyRes) => {
        if (proxyRes.statusCode !== 200) {
            return res.status(proxyRes.statusCode).json({ error: 'TTS failed' });
        }
        
        res.setHeader('Content-Type', 'audio/mpeg');
        res.setHeader('Access-Control-Allow-Origin', '*');
        proxyRes.pipe(res);
    });
    
    request.on('error', (e) => {
        res.status(500).json({ error: e.message });
    });
    
    request.end();
};