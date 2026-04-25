# Curso de Chinês - Web Application Specification

## Project Overview
- **Project Name**: Curso de Chinês (Chinese Course)
- **Type**: Web Application (Python + Flask)
- **Core Functionality**: A comprehensive Chinese language learning platform with texts, conversations, pronunciation, interactive modules, quizzes, and flashcards
- **Target Users**: Portuguese speakers learning Chinese

## Technical Stack
- **Backend**: Python with Flask
- **Frontend**: HTML/CSS/JavaScript (responsive design)
- **Text-to-Speech**: gTTS (Google TTS) for pronunciation
- **Data Storage**: JSON files (no database required)

## UI/UX Specification

### Layout Structure
- **Header**: Logo, navigation menu, user progress indicator
- **Main Content**: Dynamic content area based on current module/lesson
- **Sidebar**: Module navigation with progress bars
- **Footer**: Copyright and links

### Visual Design
- **Color Palette**:
  - Primary: #C41E3A (Chinese Red - 中国红)
  - Secondary: #FFD700 (Gold - 金色)
  - Background: #FFF8E7 (Warm White)
  - Text: #2C2C2C (Dark Gray)
  - Accent: #1E90FF (Dodger Blue for audio buttons)
- **Typography**:
  - Headings: Noto Sans SC (Chinese support)
  - Body: Arial, sans-serif
  - Chinese Text: 24px for readability
- **Spacing**: 16px base unit, 24px for sections

### Components
- **Module Cards**: Icon, title, progress bar, lock/unlock status
- **Lesson Cards**: Number, title, completion checkmark
- **Audio Player**: Play button with waveform animation
- **Flashcard**: Flip animation with Chinese/Portuguese sides
- **Quiz**: Multiple choice with immediate feedback
- **Progress Bar**: Animated with percentage

## Functionality Specification

### Modules Structure
1. **Iniciante (Beginner)**: Basic greetings, numbers 1-10, simple phrases
2. **Intermediário (Intermediate)**: Daily conversations, food, transportation
3. **Avançado (Advanced)**: Business Chinese, complex sentences
4. **Fluente (Fluent)**: Advanced topics, idioms, fluency training

### Features
1. **Lessons**: Text content with pinyin and translation
2. **Audio Pronunciation**: gTTS generated audio for all content
3. **Flashcards**: Spaced repetition with audio
4. **Quizzes**: Multiple choice with 70% passing threshold
5. **Progress Tracking**: LocalStorage based progress
6. **Module Locking**: Sequential unlocking system

### Data Structure
```json
{
  "modules": [
    {
      "id": "iniciante",
      "title": "Iniciante",
      "lessons": [
        {
          "id": "saudacoes",
          "title": "Saudações",
          "content": "Chinese text",
          "pinyin": "pinyin",
          "translation": "Portuguese translation",
          "words": [{"word": "你好", "pinyin": "nǐ hǎo", "meaning": "Olá"}]
        }
      ],
      "quiz": {"questions": [...]}
    }
  ]
}
```

### User Interactions
- Click audio button → Play pronunciation
- Click flashcard → Flip to show translation
- Submit quiz → Calculate score, show results
- Complete module → Unlock next module

## Acceptance Criteria
1. All 4 modules are accessible in navigation
2. Audio plays for all Chinese text content
3. Quiz requires 70% to pass
4. Next module is locked until previous is completed
5. Flashcards flip with animation
6. Progress is saved in browser
7. All Chinese text has pinyin and translation