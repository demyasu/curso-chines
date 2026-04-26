from flask import Flask, jsonify, request
from database import init_db, get_all_modules, get_module_by_id, get_lessons_by_module, get_lesson_by_id, get_words_by_lesson, get_quiz_by_module, get_quiz_by_lesson, add_word, add_module, add_lesson, unlock_module, search_words
import os

app = Flask(__name__)

init_db()

@app.route('/api/modules', methods=['GET'])
def api_get_modules():
    modules = get_all_modules()
    for m in modules:
        m['locked'] = bool(m['locked'])
    return jsonify(modules)

@app.route('/api/modules/<int:module_id>', methods=['GET'])
def api_get_module(module_id):
    module = get_module_by_id(module_id)
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    module['locked'] = bool(module['locked'])
    return jsonify(module)

@app.route('/api/modules/<int:module_id>/lessons', methods=['GET'])
def api_get_module_lessons(module_id):
    lessons = get_lessons_by_module(module_id)
    return jsonify(lessons)

@app.route('/api/lessons/<int:lesson_id>', methods=['GET'])
def api_get_lesson(lesson_id):
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    words = get_words_by_lesson(lesson_id)
    lesson['words'] = words
    
    return jsonify(lesson)

@app.route('/api/modules/<int:module_id>/quiz', methods=['GET'])
def api_get_module_quiz(module_id):
    questions = get_quiz_by_module(module_id)
    for q in questions:
        q['options'] = eval(q['options']) if isinstance(q['options'], str) else q['options']
    return jsonify(questions)

@app.route('/api/lessons/<int:lesson_id>/quiz', methods=['GET'])
def api_get_lesson_quiz(lesson_id):
    questions = get_quiz_by_lesson(lesson_id)
    for q in questions:
        q['options'] = eval(q['options']) if isinstance(q['options'], str) else q['options']
    return jsonify(questions)

@app.route('/api/modules/<int:module_id>/unlock', methods=['POST'])
def api_unlock_module(module_id):
    unlock_module(module_id)
    return jsonify({'success': True})

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    words = search_words(query)
    return jsonify(words)

@app.route('/api/audio', methods=['GET'])
def api_audio():
    from gtts import gTTS
    text = request.args.get('text', '')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    lang = request.args.get('lang', 'zh-CN')
    filename = f"audio_{abs(hash(text))}.mp3"
    filepath = os.path.join('static', 'audio', filename)
    full_path = os.path.join(os.path.dirname(__file__), filepath)
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    if not os.path.exists(full_path):
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(full_path)
    
    from flask import send_file
    return send_file(full_path, mimetype='audio/mpeg')

@app.route('/api/words', methods=['POST'])
def api_add_word():
    data = request.json
    word_id = add_word(
        data['lesson_id'],
        data['word'],
        data['pinyin'],
        data['meaning'],
        data.get('audio_url')
    )
    return jsonify({'id': word_id, 'success': True})

@app.route('/api/modules', methods=['POST'])
def api_add_module():
    data = request.json
    module_id = add_module(
        data['title'],
        data['title_zh'],
        data['description'],
        data['icon']
    )
    return jsonify({'id': module_id, 'success': True})

@app.route('/api/lessons', methods=['POST'])
def api_add_lesson():
    data = request.json
    lesson_id = add_lesson(
        data['module_id'],
        data['title'],
        data['title_zh'],
        data['content']
    )
    return jsonify({'id': lesson_id, 'success': True})

@app.route('/api/course', methods=['GET'])
def api_get_course():
    """Retorna o curso completo com módulos, lições e palavras"""
    modules = get_all_modules()
    for module in modules:
        module['locked'] = bool(module['locked'])
        module['lessons'] = get_lessons_by_module(module['id'])
        for lesson in module['lessons']:
            lesson['words'] = get_words_by_lesson(lesson['id'])
        module['quiz'] = {
            'questions': get_quiz_by_module(module['id'])
        }
    return jsonify({'modules': modules})

@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)