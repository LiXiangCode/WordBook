import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 数据库文件路径
db_file = 'wordbook.json'

# 检查数据库文件是否存在，如果不存在，创建一个
if not os.path.exists(db_file):
    with open(db_file, 'w') as f:
        json.dump({}, f)

def load_database():
    with open(db_file, 'r') as f:
        return json.load(f)

def save_database(database):
    with open(db_file, 'w') as f:
        json.dump(database, f, indent=4)

def add_or_update_word(word, definition=None):
    database = load_database()
    if word in database:
        print(f"单词 '{word}' 已经存在.")
        print("释义:")
        for idx, defn in enumerate(database[word]['definitions'], start=1):
            print(f"{idx}. {defn}")
        if definition and definition.lower() != 'no':
            database[word]['definitions'].append(definition)
        database[word]['count'] += 1
        print(f"这个词已经被查询了 {database[word]['count']} 次.")
    else:
        database[word] = {'count': 1, 'definitions': [definition] if definition else []}
    save_database(database)

def print_database():
    database = load_database()
    print("所有单词:")
    for word, info in database.items():
        print(f"{word}: {info['count']} 次, 释义: {', '.join(info['definitions'])}")

def generate_pdf():
    database = load_database()
    # 注册中文字体
    pdfmetrics.registerFont(TTFont('Chinese', 'STHeiti Light.ttc'))
    c = canvas.Canvas("wordbook.pdf", pagesize=letter)

    # 使用注册的中文字体
    c.setFont("Chinese", 12)

    c.drawString(100, 750, "所有单词")
    y = 730
    for word, info in database.items():
        # 格式化单词、次数和释义
        line_format = "{:<30}{:>3}   " + "   ".join(["{:<15}" for _ in info['definitions']])
        line = line_format.format(word, info['count'], *info['definitions'])

        c.drawString(100, y, line)
        y -= 20
        if y < 50:  # 如果到达页面底部，则创建新的一页
            c.showPage()
            y = 780
            c.setFont("SimSun", 10)  # 确保在新页面上设置字体
    c.save()
    print("PDF已生成: wordbook.pdf")

# 请将'YOUR_PATH_TO_TTF_FONT_FILE.ttf'替换为你的中文TTF字体文件的路径

# Example usage
while True:
    action = input("输入 '1' 添加或更新一个单词, 'p' 显示当前所有数据, 'g' 生成PDF文件, 'q' 退出: ")
    if action.lower() == 'q':
        break
    elif action.lower() == '1':
        word = input("输入一个单词: ")
        definition = input("输入释义 (输入'no'表示当前释义已存在，无需再输入): ")
        add_or_update_word(word, definition)
    elif action.lower() == 'p':
        print_database()
    elif action.lower() == 'g':
        generate_pdf()