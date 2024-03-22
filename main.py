import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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

def add_or_update_word(word):
    database = load_database()
    if word in database:
        print(f"单词 '{word}' 已经存在.")
        print("释义:")
        for idx, defn in enumerate(database[word]['definitions'], start=1):
            print(f"{idx}.{defn} ")
        quote = input("是否添加新释义(y/n)?: ")
        if quote == 'y':
            definition = input("新释义: ")
            database[word]['definitions'].append(definition)
        # if definition and definition.lower() != 'no':
        #     database[word]['definitions'].append(definition)
        database[word]['count'] += 1
        #print(f"这个词已经被查询了 {database[word]['count']} 次.")
    else:
        definition = input("请输入释义: ")  
        verb_es = input("输出入第三人称单数: ")
        verb_ing = input("请输入ing形式: ")
        verb_past = input("请输入过去式: ")
        verb_participle = input("请输入过去分词: ")
        database[word] = {'count': 1, 'verb_es': verb_es, 'verb_ing': verb_ing, 
                          'verb_past': verb_past, 'verb_participle': verb_participle,
                          'definitions': [definition] if definition else []}
    save_database(database)

def print_database():
    database = load_database()
    print("所有单词:")
    for word, info in database.items():
        print(f"{word}: {info['count']} 次, 释义: {', '.join(info['definitions'])}")


def generate_pdf():
    database = load_database()
    # 注册中文字体以支持中文
    pdfmetrics.registerFont(TTFont('Chinese', 'STHeiti Light.ttc'))
    # 创建PDF文档
    doc = SimpleDocTemplate("wordbook_with_table.pdf", pagesize=letter)
    page_width, page_height = letter
    margin = 30
    # 准备表格数据
    table_data = [['单词', '记忆次数', '释义']]
    for word, info in database.items():
        # 将释义列表转换成字符串，并加入表格数据中
        definitions = ', '.join(info['definitions'])
        table_data.append([word, str(info['count']), definitions])
    # 创建表格实例
    table = Table(table_data)
    # 指定每列的宽度
    colWidths = [100, 50, 200]  # 例如，第一列100点，第二列50点，第三列200点宽

    # 指定每行的高度
    rowHeights = [20] * len(table_data)  # 每行20点高    
    # 创建表格样式
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('ROWHEIGHTS', (0, 0), (-1, -1), rowHeights),
        ('COLWIDTHS', (0, 0), (-1, -1), colWidths),
    ]))
    # 构建PDF文档g
    doc.build([table])
    print("PDF文档已生成: wordbook_with_table.pdf")


# Example usage
while True:
    word = input("输入一个单词: ")
    if word.lower() == 'q':
        break
    elif word.lower() == 'g':
        generate_pdf()
    elif word.lower() == 'p':
        print_database()
    else:      
        add_or_update_word(word)
    # action = input("输入 '1' 添加或更新一个单词, 'p' 显示当前所有数据, 'g' 生成PDF文件, 'q' 退出: ")
    # if action.lower() == 'q':
    #     break
    # elif action.lower() == '1':
    #     word = input("输入一个单词: ")
    #     definition = input("输入释义 (输入'no'表示当前释义已存在，无需再输入): ")
    #     add_or_update_word(word, definition)
    # elif action.lower() == 'p':
    #     print_database()
    # elif action.lower() == 'g':
    #     generate_pdf()
