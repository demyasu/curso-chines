const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const courseData = require('./course_data.json');

app.use(express.json());

// API Routes
app.get('/api/course', (req, res) => {
    const modules = courseData.modules.map((m, idx) => ({
        ...m,
        numericId: idx + 1,
        word_count: m.lessons.reduce((sum, l) => sum + (l.words?.length || 0), 0),
        locked: m.locked || false
    }));
    res.json({ modules });
});

app.get('/api/modules', (req, res) => {
    res.json(courseData.modules.map((m, idx) => ({
        id: m.id,
        numericId: idx + 1,
        title: m.title,
        title_zh: m.title_zh,
        locked: m.locked || false
    })));
});

app.get('/api/modules/:id/lessons', (req, res) => {
    const moduleId = req.params.id;
    const module = courseData.modules.find(m => 
        m.id == moduleId || m.id === moduleId || 
        String(modules.indexOf(m) + 1) === moduleId
    );
    
    if (!module) {
        return res.status(404).json({ error: 'Module not found' });
    }
    
    const lessons = module.lessons.map((l, idx) => ({
        ...l,
        numericId: idx + 1,
        word_count: l.words?.length || 0
    }));
    
    res.json(lessons);
});

app.get('/api/lessons/:id', (req, res) => {
    const lessonId = req.params.id;
    
    for (const module of courseData.modules) {
        const lesson = module.lessons.find((l, idx) => 
            l.id == lessonId || l.id === lessonId || 
            String(module.lessons.indexOf(l) + 1) === lessonId
        );
        if (lesson) return res.json(lesson);
    }
    
    res.status(404).json({ error: 'Lesson not found' });
});

app.get('/api/modules/:id/quiz', (req, res) => {
    const moduleId = req.params.id;
    const module = courseData.modules.find(m => 
        m.id == moduleId || m.id === moduleId || 
        String(courseData.modules.indexOf(m) + 1) === moduleId
    );
    
    if (!module) {
        return res.status(404).json({ error: 'Module not found' });
    }
    
    res.json(module.quiz?.questions || []);
});

// Health check
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Static files
app.use(express.static(path.join(__dirname, 'static')));
app.use(express.static(path.join(__dirname, 'templates')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});

process.on('SIGTERM', () => {
    process.exit(0);
});