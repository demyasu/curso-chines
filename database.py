import sqlite3
from datetime import datetime

DATABASE = 'chinese_course.db'

def get_db():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_zh TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            level_order INTEGER,
            locked INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER,
            title TEXT NOT NULL,
            title_zh TEXT NOT NULL,
            content TEXT,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER,
            word TEXT NOT NULL,
            pinyin TEXT,
            meaning TEXT,
            audio_url TEXT,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER,
            module_id INTEGER,
            question TEXT NOT NULL,
            options TEXT,
            answer INTEGER,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id),
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            module_id INTEGER,
            lesson_id INTEGER,
            completed INTEGER DEFAULT 0,
            quiz_score INTEGER,
            last_accessed TEXT,
            FOREIGN KEY (module_id) REFERENCES modules(id),
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
    ''')

    if cursor.execute('SELECT COUNT(*) FROM modules').fetchone()[0] == 0:
        seed_database(cursor)
    
    # if cursor.execute('SELECT COUNT(*) FROM words').fetchone()[0] < 100:
    #     seed_words_for_all_lessons()

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def seed_database(cursor):
    modules_data = [
        ("Iniciante", "初级", "Aprenda o básico do chinês: saudações, números e frases simples", "🌱", 1, 0),
        ("Intermediário", "中级", "Conversas do dia a dia: comida, transporte e compras", "🌿", 2, 1),
        ("Avançado", "高级", "Chinês de negócios e frases complexas", "🌳", 3, 1),
        ("Fluente", "精通", "Domínio completo do chinês: expressões idiomáticas e fluência", "🏆", 4, 1),
    ]

    cursor.executemany('''
        INSERT INTO modules (title, title_zh, description, icon, level_order, locked)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', modules_data)

    lessons_data = [
        (1, "Saudações", "问候", "你好-Olá\n再见-Adeus\n早上好-Bom dia\n晚上好-Boa noite\n晚安-Boas noches\n谢谢-Obrigado\n不客气-De nada\n对不起-Desculpe\n没关系-Não tem problema\n你好吗-Como está você?"),
        (1, "Números", "数字", "一-Um\n二-Dois\n三-Três\n四-Quatro\n五-Cinco\n六-Seis\n七-Sete\n八-Oito\n九-Nove\n十-Dez"),
        (1, "Introdução Pessoal", "自我介绍", "我叫…-Meu nome é…\n我是…-Eu sou…\n我来自…-Eu vim de…\n很高兴认识你-Prazer em conhecê-lo\n你是哪国人-De qual país você é?"),
        (1, "Família", "家庭", "爸爸-Pai\n妈妈-Mãe\n哥哥-Irmão mais velho\n姐姐-Irmã mais velha\n弟弟-Irmão mais novo\n妹妹-Irmã mais nova\n朋友-Amigo\n老师-Professor\n学生-Estudante\n先生-Senhor"),
        (1, "Cores", "颜色", "红色-Vermelho\n蓝色-Azul\n绿色-Verde\n黄色-Amarelo\n白色-Branco\n黑色-Preto\n紫色-Roxo\n橙色-Laranja\n粉色-Rosa\n棕色-Marrom"),
        (2, "Comida e Restaurante", "餐饮", "我要这个-Eu quero este\n多少钱-Quanto custa?\n太贵了-Muito caro\n便宜点-Mais barato\n好吃-Delicioso\n我要买单-A conta\n有菜单吗-Tem menu?"),
        (2, "Transporte", "交通", "出租车-Táxi\n公交车-Ônibus\n地铁-Metrô\n飞机-Avião\n请问…在哪里-Onde fica…?\n我要去…-Eu quero ir para…\n左边-Esquerda\n右边-Direita"),
        (2, "Compras", "购物", "这个多少钱-Quanto custa isto?\n可以便宜点吗-Pode ser mais barato?\n太小了-Muito pequeno\n太大了-Muito grande\n正好-Perfeito\n我买了-Eu compro"),
        (2, "Tempo e Dias", "时间和日期", "今天-Hoje\n明天-Amanhã\n昨天-Ontem\n现在-Agora\n几点-Que horas?\n星期一-Segunda-feira\n星期二-Terça-feira\n星期三-Quarta-feira\n星期四-Quinta-feira\n星期五-Sexta-feira"),
        (2, "Lugares", "地方", "医院-Hospital\n银行-Banco\n超市-Supermercado\n餐厅-Restaurante\n学校-Escola\n图书馆-Biblioteca\n公园-Parque\n火车站-Estação de trem\n机场-Aeroporto\n商场-Shopping"),
        (3, "Negócios", "商务", "很高兴见到您-Prazer em conhecê-lo\n我们可以讨论一下吗-Podemos discutir?\n请问您的预算是多少-Qual é seu orçamento?\n我们需要再考虑一下-Precisamos considerar\n合同-Contrato\n会议-Reunião\n报价-Cotação"),
        (3, "Expressões Avançadas", "高级表达", "说实话-Para ser honesto\n一般来说-Em geral\n除此之外-Além disso\n事实上-Na verdade\n更重要的是-Mais importante\n我认为-Eu acho que\n不管怎样-De qualquer forma"),
        (3, "Emoções e Opiniões", "情感", "我感到…-Eu sinto…\n我很喜欢…-Eu gosto muito de…\n我不太确定…-Eu não tenho certeza…\n这让我感到…-Isto me faz sentir…\n我希望能…-Eu espero poder…"),
        (3, "Comunicação por Telefone", "电话", "请问您是哪位-Quem é?\n请稍等-Aguarde um momento\n我现在不方便-Não é conveniente agora\n我可以给您回电话吗-Posso retornar?\n您的电话号码是多少-Qual é seu número?"),
        (3, "Ambiente de Trabalho", "工作", "办公室-Escritório\n公司-Empresa\n同事-Colega\n老板-Chefe\n加班-Horas extras\n请假-Pedir licença\n出差-Viagem de negócios\n辞职-Demitir-se"),
        (4, "Expressões Idiomáticas", "成语", "一帆风顺-Bom sucesso\n画蛇添足-Exagerar\n守株待兔-Esperar sem fazer nada\n胸有成竹-Ter confiança\n滴水穿石-Persistência\n亡羊补牢-É melhor tarde do que nunca\n塞翁失马-Bênção disfarçada"),
        (4, "Conversas Avançadas", "高级对话", "你觉得…怎么样-O que você acha de…?\n如果…的话-Se…\n虽然…但是…-Embora…no entanto…\n除非…否则…-A menos que…caso contrário…\n不但…而且…-Não só…mas também…"),
        (4, "Introdução à Literatura", "文学", "古诗-Poesia clássica\n论语-Os Analectos\n唐诗-Poesia Tang\n小说-Romance\n汉字-Caracteres chineses\n文化-Cultura\n历史-História"),
        (4, "Filosofia Chinesa", "哲学", "孔子-Confúcio\n老子-Laozi\n道-O Caminho\n德-Virtude\n阴阳-Yin e Yang\n八卦-Oito Trigramas\n天命-Mandato do Céu"),
        (4, "Expressões Regionais", "方言", "普通话-Mandarim padrão\n广东话-Cantonês\n上海话-Shanghainês\n东北话-Dialeto do Nordeste\n儿化-Sufixo er\n方言-Dialeto regional\n口音-Sotaque"),
    ]

    cursor.executemany('''
        INSERT INTO lessons (module_id, title, title_zh, content)
        VALUES (?, ?, ?, ?)
    ''', lessons_data)

    words_data = [
        (1, "你好", "nǐ hǎo", "Olá"),
        (1, "再见", "zài jiàn", "Adeus"),
        (1, "早上好", "zǎo shang hǎo", "Bom dia"),
        (1, "晚上好", "wǎn shang hǎo", "Boa noite"),
        (1, "晚安", "wǎn ān", "Boa noite"),
        (1, "谢谢", "xiè xie", "Obrigado"),
        (1, "不客气", "bù kè qì", "De nada"),
        (1, "对不起", "duì bu qǐ", "Desculpe"),
        (1, "没关系", "méi guān xi", "Não tem problema"),
        (1, "你好吗", "nǐ hǎo ma", "Como está você?"),
        (2, "一", "yī", "Um"),
        (2, "二", "èr", "Dois"),
        (2, "三", "sān", "Três"),
        (2, "四", "sì", "Quatro"),
        (2, "五", "wǔ", "Cinco"),
        (2, "六", "liù", "Seis"),
        (2, "七", "qī", "Sete"),
        (2, "八", "bā", "Oito"),
        (2, "九", "jiǔ", "Nove"),
        (2, "十", "shí", "Dez"),
    ]

    cursor.executemany('''
        INSERT INTO words (lesson_id, word, pinyin, meaning)
        VALUES (?, ?, ?, ?)
    ''', words_data)

    quiz_data = [
        # Saudações (lesson 1)
        (1, 1, "Como se diz 'Olá' em chinês?", '["你好","再见","谢谢","不客气"]', 0),
        (1, 1, "O que significa '再见'?", '["Olá","Adeus","Obrigado","De nada"]', 1),
        (1, 1, "Como se diz 'Obrigado'?", '["你好","谢谢","对不起","没关系"]', 1),
        
        # Números (lesson 2)
        (2, 1, "Qual é o número '一'?", '["1","2","3","4"]', 0),
        (2, 1, "Como se diz 'três' em chinoês?", '["一","二","三","四"]', 2),
        (2, 1, "Qual número vem depois de '七'?", '["六","八","九","十"]', 1),
        
        # Introdução Pessoal (lesson 3)
        (3, 1, "Como se diz 'Meu nome é'?", '["我叫","我是","我来","你去"]', 0),
        (3, 1, "O que significa '我来自'?", '["Eu sou","Eu vim de","Eu vou","Eu como"]', 1),
        (3, 1, "Como perguntar 'De qual país você é?'", '["你是哪国人","你吃什么","你去哪里","你叫什么"]', 0),
        
        # Família (lesson 4)
        (4, 1, "Como se diz 'Pai' em chinês?", '["爸爸","妈妈","老师","学生"]', 0),
        (4, 1, "O que significa '妈妈'?", '["Pai","Mãe","Irmão","Filho"]', 1),
        (4, 1, "Como se diz 'amigo'?", '["朋友","老师","学生","同事"]', 0),
        
        # Cores (lesson 5)
        (5, 1, "Como se diz 'vermelho'?", '["红色","蓝色","绿色","黄色"]', 0),
        (5, 1, "O que significa '蓝色'?", '["Vermelho","Azul","Verde","Amarelo"]', 1),
        (5, 1, "Como se diz 'preto'?", '["白色","黑色","紫色","棕色"]', 1),
        
        # Comida (lesson 6)
        (6, 2, "Como pedir 'Eu quero este'?", '["我要这个","吃什么","喝什么","去哪儿"]', 0),
        (6, 2, "O que significa '好吃'?", '["Caro","Barato","Delicioso","Não"]', 2),
        (6, 2, "Como pedir a conta?", '["买单","菜单","好吃","便宜"]', 0),
        
        # Transporte (lesson 7)
        (7, 2, "Como se diz 'táxi'?", '["出租车","公交车","地铁","飞机"]', 0),
        (7, 2, "O que significa '地铁'?", '["Táxi","Ônibus","Metrô","Avião"]', 2),
        (7, 2, "Como se diz 'esquerda'?", '["左边","右边","前边","后边"]', 0),
        
        # Compras (lesson 8)
        (8, 2, "Como perguntar 'Quanto custa?'", '["多少钱","吃什么","去哪儿","买什么"]', 0),
        (8, 2, "O que significa '太小了'?", '["Muito grande","Muito pequeno","Perfeito","Barato"]', 1),
        (8, 2, "Como se diz 'perfeito'?", '["可以","太小了","正好","太贵了"]', 2),
        
        # Tempo (lesson 9)
        (9, 2, "Como se diz 'hoje'?", '["今天","明天","昨天","现在"]', 0),
        (9, 2, "O que significa '明天'?", '["Hoje","Amanhã","Ontem","Agora"]', 1),
        (9, 2, "Qual dia é 'segunda-feira'?", '["星期二","星期一","星期三","星期四"]', 1),
        
        # Lugares (lesson 10)
        (10, 2, "Como se diz 'hospital'?", '["医院","银���","学校","餐厅"]', 0),
        (10, 2, "O que significa '银行'?", '["Hospital","Banco","Escola","Restaurante"]', 1),
        (10, 2, "Como se diz 'parque'?", '["公园","图书馆","商场","超市"]', 0),
        
        # Negócios (lesson 11)
        (11, 3, "Como se diz 'contrato'?", '["合同","会议","报价","公司"]', 0),
        (11, 3, "O que significa '会议'?", '["Contrato","Reunião","Orçamento","Empresa"]', 1),
        (11, 3, "Como se diz 'cotação'?", '["合同","会议","报价","公司"]', 2),
        
        # Expressões Avançadas (lesson 12)
        (12, 3, "Como se diz 'para ser honesto'?", '["说实话","一般来说","事实上","我认为"]', 0),
        (12, 3, "O que significa '一般来说'?", '["Para ser honesto","Em geral","Na verdade","Eu acho que"]', 1),
        (12, 3, "Como se diz 'eu acho que'?", '["我知道","我认为","我感到","我希望"]', 1),
        
        # Emoções (lesson 13)
        (13, 3, "Como se diz 'eu sinto'?", '["我感到","我很喜欢","我不太确定","我希望"]', 0),
        (13, 3, "O que significa '我很喜欢'?", '["Eu sinto","Eu gosto muito de","Eu não sei","Eu espero"]', 1),
        (13, 3, "Como se diz 'eu espero'?", '["我感到","我很喜欢","我不太确定","我希望"]', 3),
        
        # Telefone (lesson 14)
        (14, 3, "Como perguntar 'Quem é?'?", '["请问您是哪位","请稍等","我现在不方便","您电话号码"]', 0),
        (14, 3, "O que significa '请稍等'?", '["Quem é?","Aguarde um momento","Não é conveniente","Número de telefone"]', 1),
        (14, 3, "Como se diz 'posso retornar?'?", '["我可以回电话吗","您是哪位","请稍等","现在不方便"]', 0),
        
        # Trabalho (lesson 15)
        (15, 3, "Como se diz 'escritório'?", '["办公室","公司","同事","老板"]', 0),
        (15, 3, "O que significa '加班'?", '["Férias","Horas extras","Licença","Viagem"]', 1),
        (15, 3, "Como se diz 'chefe'?", '["同事","老板","公司","员工"]', 1),
        
        # Expressões Idiomáticas (lesson 16)
        (16, 4, "O que significa '一帆风顺'?", '["Falhar","Bom sucesso","Esperar","Persistência"]', 1),
        (16, 4, "Como se diz 'Confúcio'?", '["老子","孔子","皇帝","天使"]', 1),
        (16, 4, "O que significa '道'?", '["Virtude","Caminho","Poder","Saber"]', 1),
        
        # Conversas Avançadas (lesson 17)
        (17, 4, "Como se diz 'se...'?", '["如果","虽然","除非","否则"]', 0),
        (17, 4, "O que significa '虽然...但是'?", '["Se...então","Embora...no entanto","A menos que...caso contrário","Não só...mas também"]', 1),
        (17, 4, "Como se diz 'o que você acha?'?", '["你觉得怎么样","如果","虽然","除非"]', 0),
        
        # Literatura (lesson 18)
        (18, 4, "Como se diz 'poesia clássica'?", '["古诗","唐诗","小说","论语"]', 0),
        (18, 4, "O que significa '小说'?", '["Poesia","Romance","Cultura","História"]', 1),
        (18, 4, "Como se diz 'caracteres chineses'?", '["汉字","文化","历史","古诗"]', 0),
        
        # Filosofia (lesson 19)
        (19, 4, "Como se diz 'Confúcio'?", '["孔子","老子","道德","天命"]', 0),
        (19, 4, "O que significa '阴阳'?", '["Yin e Yang","Oito Trigramas","Mandato do Céu","Virtude"]', 0),
        (19, 4, "Como se diz 'o Caminho'?", '["道","德","天命","阴阳"]', 0),
        
        # Expressões Regionais (lesson 20)
        (20, 4, "O que significa '普通话'?", '["Cantonês","Mandarim padrão","Shanghainês","Dialeto"]', 1),
        (20, 4, "Como se diz 'cantonês'?", '["普通话","广东话","上海话","东北话"]', 1),
        (20, 4, "O que significa '口音'?", '["Sotaque","Dialeto","Sufixo er","Mandarim"]', 0),
    ]

    cursor.executemany('''
        INSERT INTO quiz_questions (lesson_id, module_id, question, options, answer)
        VALUES (?, ?, ?, ?, ?)
    ''', quiz_data)

def get_all_modules():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.*, 
               COUNT(DISTINCT l.id) as lesson_count,
               COUNT(DISTINCT w.id) as word_count
        FROM modules m
        LEFT JOIN lessons l ON l.module_id = m.id
        LEFT JOIN words w ON w.lesson_id = l.id
        GROUP BY m.id
        ORDER BY m.level_order
    ''')
    modules = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return modules

def get_module_by_id(module_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM modules WHERE id = ?', (module_id,))
    module = cursor.fetchone()
    conn.close()
    return dict(module) if module else None

def get_lessons_by_module(module_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, COUNT(w.id) as word_count
        FROM lessons l
        LEFT JOIN words w ON w.lesson_id = l.id
        WHERE l.module_id = ?
        GROUP BY l.id
    ''', (module_id,))
    lessons = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return lessons

def get_lesson_by_id(lesson_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
    lesson = cursor.fetchone()
    conn.close()
    return dict(lesson) if lesson else None

def get_words_by_lesson(lesson_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words WHERE lesson_id = ?', (lesson_id,))
    words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return words

def get_quiz_by_module(module_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quiz_questions WHERE module_id = ?', (module_id,))
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions

def get_quiz_by_lesson(lesson_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quiz_questions WHERE lesson_id = ?', (lesson_id,))
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions

def add_word(lesson_id, word, pinyin, meaning, audio_url=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO words (lesson_id, word, pinyin, meaning, audio_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (lesson_id, word, pinyin, meaning, audio_url))
    word_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return word_id

def add_words_batch(words_list):
    conn = get_db()
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO words (lesson_id, word, pinyin, meaning)
        VALUES (?, ?, ?, ?)
    ''', words_list)
    conn.commit()
    conn.close()

def seed_words_for_all_lessons():
    all_words = [
        (3, "我叫", "wǒ jiào", "Meu nome é"),
        (3, "我来自", "wǒ láizì", "Eu vim de"),
        (3, "很高兴认识你", "hěn gāoxìng rènshi nǐ", "Prazer em conhecê-lo"),
        (3, "你是哪国人", "nǐ shì nǎ guó rén", "De qual país você é?"),
        (4, "爸爸", "bàba", "Pai"),
        (4, "妈妈", "māma", "Mãe"),
        (4, "哥哥", "gēge", "Irmão mais velho"),
        (4, "姐姐", "jiějie", "Irmã mais velha"),
        (4, "弟弟", "dìdi", "Irmão mais novo"),
        (4, "妹妹", "mèimei", "Irmã mais nova"),
        (4, "朋友", "péngyou", "Amigo"),
        (4, "老师", "lǎoshī", "Professor"),
        (4, "学生", "xuéshēng", "Estudante"),
        (4, "先生", "xiānsheng", "Senhor"),
        (5, "红色", "hóngsè", "Vermelho"),
        (5, "蓝色", "lánsè", "Azul"),
        (5, "绿色", "lǜsè", "Verde"),
        (5, "黄色", "huángsè", "Amarelo"),
        (5, "白色", "báisè", "Branco"),
        (5, "黑色", "hēisè", "Preto"),
        (5, "紫色", "zǐsè", "Roxo"),
        (5, "橙色", "chéngsè", "Laranja"),
        (5, "粉色", "fěnsè", "Rosa"),
        (5, "棕色", "zōngsè", "Marrom"),
        (6, "我要这个", "wǒ yào zhège", "Eu quero este"),
        (6, "多少钱", "duōshao qián", "Quanto custa?"),
        (6, "太贵了", "tài guì le", "Muito caro"),
        (6, "好吃", "hǎochī", "Delicioso"),
        (6, "我要买单", "wǒ yào mǎidān", "A conta"),
        (6, "有菜单吗", "yǒu càidān ma", "Tem menu?"),
        (7, "出租车", "chūzū chē", "Táxi"),
        (7, "公交车", "gōngjiāo chē", "Ônibus"),
        (7, "地铁", "dìtiě", "Metrô"),
        (7, "飞机", "fēijī", "Avião"),
        (7, "左边", "zuǒbiān", "Esquerda"),
        (7, "右边", "yòubiān", "Direita"),
        (8, "这个多少钱", "zhège duōshao qián", "Quanto custa isto?"),
        (8, "可以便宜点吗", "kěyǐ piányi diǎn ma", "Pode ser mais barato?"),
        (8, "太小了", "tài xiǎo le", "Muito pequeno"),
        (8, "太大了", "tài dà le", "Muito grande"),
        (8, "正好", "zhènghǎo", "Perfeito"),
        (8, "我买了", "wǒ mǎi le", "Eu compro"),
        (9, "今天", "jīntiān", "Hoje"),
        (9, "明天", "míngtiān", "Amanhã"),
        (9, "昨天", "zuótiān", "Ontem"),
        (9, "现在", "xiànzài", "Agora"),
        (9, "几点", "jǐ diǎn", "Que horas?"),
        (9, "星期一", "xīngqī yī", "Segunda-feira"),
        (9, "星期二", "xīngqī èr", "Terça-feira"),
        (9, "星期三", "xīngqī sān", "Quarta-feira"),
        (9, "星期四", "xīngqī sì", "Quinta-feira"),
        (9, "星期五", "xīngqī wǔ", "Sexta-feira"),
        (10, "医院", "yīyuàn", "Hospital"),
        (10, "银行", "yínháng", "Banco"),
        (10, "超市", "chāoshì", "Supermercado"),
        (10, "餐厅", "cāntīng", "Restaurante"),
        (10, "学校", "xuéxiào", "Escola"),
        (10, "图书馆", "túshūguǎn", "Biblioteca"),
        (10, "公园", "gōngyuán", "Parque"),
        (10, "火车站", "huǒchē zhàn", "Estação de trem"),
        (10, "机场", "jīchǎng", "Aeroporto"),
        (10, "商场", "shāngchǎng", "Shopping"),
        (11, "合同", "hétong", "Contrato"),
        (11, "会议", "huìyì", "Reunião"),
        (11, "报价", "bàojià", "Cotação"),
        (11, "我们可以讨论一下吗", "wǒmen kěyǐ tǎolùn yīxià ma", "Podemos discutir?"),
        (12, "说实话", "shuō shíhuà", "Para ser honesto"),
        (12, "一般来说", "yībān lái shuō", "Em geral"),
        (12, "除此之外", "chú cǐ zhī wài", "Além disso"),
        (12, "事实上", "shìshí shàng", "Na verdade"),
        (12, "更重要的是", "gèng zhòngyào de shì", "Mais importante"),
        (12, "我认为", "wǒ rènwéi", "Eu acho que"),
        (13, "我感到", "wǒ gǎndào", "Eu sinto"),
        (13, "我很喜欢", "wǒ hěn xǐhuan", "Eu gosto muito de"),
        (13, "我不太确定", "wǒ bù tài quèdìng", "Eu não tenho certeza"),
        (13, "我希望", "wǒ xīwàng", "Eu espero"),
        (14, "请问您是哪位", "qǐng wèn nín shì nǎ wèi", "Quem é?"),
        (14, "请稍等", "qǐng shāo děng", "Aguarde um momento"),
        (14, "我现在不方便", "wǒ xiànzài bù fāngbiàn", "Não é conveniente agora"),
        (14, "我可以给您回电话吗", "wǒ kěyǐ gěi nín huí diànhuà ma", "Posso retornar?"),
        (15, "办公室", "bàngōngshì", "Escritório"),
        (15, "公司", "gōngsī", "Empresa"),
        (15, "同事", "tóngshì", "Colega"),
        (15, "老板", "lǎobǎn", "Chefe"),
        (15, "加班", "jiābān", "Horas extras"),
        (15, "请假", "qǐngjià", "Pedir licença"),
        (15, "出差", "chūchāi", "Viagem de negócios"),
        (15, "辞职", "cízhí", "Demitir-se"),
        (16, "一帆风顺", "yī fān fēng shùn", "Bom sucesso"),
        (16, "画蛇添足", "huà shé tiān zú", "Exagerar"),
        (16, "守株待兔", "shǒu zhū dài tù", "Esperar sem fazer nada"),
        (16, "胸有成竹", "xiōng yǒu chéng zhú", "Ter confiança"),
        (16, "滴水穿石", "dī shuǐ chuān shí", "Persistência"),
        (16, "亡羊补牢", "wáng yáng bǔ láo", "É melhor tarde do que nunca"),
        (16, "塞翁失马", "sàiwēng shī mǎ", "Bênção disfarçada"),
        (17, "你觉得怎么样", "nǐ juéde zěnmeyàng", "O que você acha?"),
        (17, "如果", "rúguǒ", "Se"),
        (17, "虽然", "suīrán", "Embora"),
        (17, "但是", "dànshì", "No entanto"),
        (17, "除非", "chúfēi", "A menos que"),
        (17, "否则", "fǒuzé", "Caso contrário"),
        (18, "古诗", "gǔshī", "Poesia clássica"),
        (18, "论语", "lúnyǔ", "Os Analectos"),
        (18, "唐诗", "tángshī", "Poesia Tang"),
        (18, "小说", "xiǎoshuō", "Romance"),
        (18, "汉字", "hànzì", "Caracteres chineses"),
        (18, "文化", "wénhuà", "Cultura"),
        (18, "历史", "lìshǐ", "História"),
        (19, "孔子", "kǒngzǐ", "Confúcio"),
        (19, "老子", "lǎozǐ", "Laozi"),
        (19, "道", "dào", "O Caminho"),
        (19, "德", "dé", "Virtude"),
        (19, "阴阳", "yīnyáng", "Yin e Yang"),
        (19, "八卦", "bāguà", "Oito Trigramas"),
        (19, "天命", "tiānmìng", "Mandato do Céu"),
        (20, "普通话", "pǔtōnghuà", "Mandarim padrão"),
        (20, "广东话", "guǎngdōnghuà", "Cantonês"),
        (20, "上海话", "shànghǎihuà", "Shanghainês"),
        (20, "东北话", "dōngběihuà", "Dialeto do Nordeste"),
        (20, "儿化", "érhuà", "Sufixo er"),
        (20, "方言", "fāngyán", "Dialeto regional"),
        (20, "口音", "kǒuyīn", "Sotaque"),
    ]
    add_words_batch(all_words)

def add_module(title, title_zh, description, icon):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(level_order) FROM modules')
    max_order = cursor.fetchone()[0] or 0
    cursor.execute('''
        INSERT INTO modules (title, title_zh, description, icon, level_order, locked)
        VALUES (?, ?, ?, ?, ?, 1)
    ''', (title, title_zh, description, icon, max_order + 1))
    module_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return module_id

def add_lesson(module_id, title, title_zh, content):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lessons (module_id, title, title_zh, content)
        VALUES (?, ?, ?, ?)
    ''', (module_id, title, title_zh, content))
    lesson_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lesson_id

def unlock_module(module_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE modules SET locked = 0 WHERE id = ?', (module_id,))
    cursor.execute('SELECT level_order FROM modules WHERE id = ?', (module_id,))
    result = cursor.fetchone()
    if result:
        current_order = result[0]
        cursor.execute('UPDATE modules SET locked = 0 WHERE level_order = ?', (current_order + 1,))
    conn.commit()
    conn.close()

def search_words(query):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT w.*, l.title as lesson_title, m.title as module_title
        FROM words w
        JOIN lessons l ON l.id = w.lesson_id
        JOIN modules m ON m.id = l.module_id
        WHERE w.word LIKE ? OR w.pinyin LIKE ? OR w.meaning LIKE ?
        ORDER BY m.level_order, l.id
    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
    words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return words