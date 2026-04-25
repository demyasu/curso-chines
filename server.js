const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const courseData = require('./course_data.json');

app.use(express.json());

// API Routes
app.get('/health', (req, res) => {
    res.type('json').send(JSON.stringify({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        version: '1.0.0'
    }));
});

app.get('/api/course', (req, res) => {
    const modules = courseData.modules.map(m => ({
        ...m,
        word_count: m.lessons.reduce((sum, l) => sum + (l.words?.length || 0), 0),
        locked: m.locked || false
    }));
    res.json({ modules });
});

app.get('/api/modules', (req, res) => {
    res.json(courseData.modules.map(m => ({
        id: m.id,
        title: m.title,
        title_zh: m.title_zh,
        locked: m.locked || false
    })));
});

app.get('/api/modules/:id/lessons', (req, res) => {
    const moduleId = req.params.id;
    const module = courseData.modules.find(m => m.id == moduleId || m.id === moduleId);
    if (!module) return res.status(404).json({ error: 'Module not found' });
    const lessons = module.lessons.map(l => ({
        ...l,
        word_count: l.words?.length || 0
    }));
    res.json(lessons);
});

app.get('/api/lessons/:id', (req, res) => {
    const lessonId = req.params.id;
    for (const module of courseData.modules) {
        const lesson = module.lessons.find(l => l.id == lessonId || l.id === lessonId);
        if (lesson) return res.json(lesson);
    }
    res.status(404).json({ error: 'Lesson not found' });
});

app.get('/api/modules/:id/quiz', (req, res) => {
    const moduleId = req.params.id;
    const module = courseData.modules.find(m => m.id == moduleId || m.id === moduleId);
    if (!module) return res.status(404).json({ error: 'Module not found' });
    res.json(module.quiz?.questions || []);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`   Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`   Health check: http://localhost:${PORT}/health`);
});

process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    process.exit(0);
});