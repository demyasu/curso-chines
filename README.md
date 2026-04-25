# Curso de Chinês - 中文课程

Aplicação web para aprendizado de chinês mandarim, projetada para falantes de português.

## Funcionalidades

- 📚 Módulos organizados por nível (Iniciante a Fluente)
- 📝 Lições com conteúdo, pinyin e tradução
- 🔊 Áudio com pronúncia nativa (Web Speech API)
- 📇 Flashcards interativos
- 📝 Quiz com pontuação
- 🔓 Sistema de desbloqueio de módulos
- 💾 Persistência de progresso no localStorage

## Stack

- **Backend**: Node.js + Express
- **Banco de Dados**: SQLite (better-sqlite3)
- **Frontend**: HTML5 + CSS3 + JavaScript Vanilla
- **Áudio**: Web Speech API (navegador)

## Deploy

### Render.com (Gratuito)

1. Fork este repositório no GitHub
2. Acesse [render.com](https://render.com)
3. Conecte seu GitHub
4. Crie um novo "Web Service"
5. Configure:
   - **Build Command**: `npm install`
   - **Start Command**: `node server.js`
   - **Plan**: Free

### Railway.app (Gratuito)

1. Fork este repositório
2. Acesse [railway.app](https://railway.app)
3. New Project > Deploy from GitHub
4. Selecione o repositório

### Local

```bash
npm install
node server.js
# Acesse http://localhost:3000
```

## API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/course` | Retorna curso completo |
| GET | `/api/modules` | Lista todos os módulos |
| GET | `/api/modules/:id/lessons` | Lista lições do módulo |
| GET | `/api/lessons/:id` | Detalhes da lição |
| GET | `/api/modules/:id/quiz` | Quiz do módulo |
| POST | `/api/words` | Adicionar palavra |
| POST | `/api/modules` | Adicionar módulo |
| POST | `/api/lessons` | Adicionar lição |

## Estrutura

```
├── server.js          # Servidor Node.js
├── database.js        # Funções do banco (legacy)
├── app.py            # Flask (legacy, não usar)
├── chinese_course.db  # Banco SQLite
├── package.json
├── static/
│   └── audio/        # Áudio gerado
└── templates/
    └── index.html    # Frontend
```

## License

MIT