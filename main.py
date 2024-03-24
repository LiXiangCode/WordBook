import datetime
import json
import os
import random
from tkinter import CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



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
            print(f"{idx}. {defn}")
        definition = input("请输入新释义,no表示不添加: ")
        if definition and definition.lower() != 'no':
            database[word]['definitions'].append(definition)
    else:
        definition = input("请输入释义: ")
        database[word] = {'count': 1, 'definitions': [definition] if definition else []}
    save_database(database)

def print_database():
    database = load_database()
    # print("所有单词:")
    # for word, info in database.items():
    #     print(f"{word}: {info['count']} 次, 释义: {', '.join(info['definitions'])}")
    #     for definition in info['definitions']:
    #         print(f"")

def generate_pdf():
    # 加载JSON文件
    database = load_database()
    # 注册中文字体以支持中文
    pdfmetrics.registerFont(TTFont('Chinese', 'STHeiti Light.ttc'))
    # 创建PDF文档
    doc = SimpleDocTemplate("wordbook_with_table.pdf", pagesize=letter)
    # 准备表格数据
    table_data = [['单词', '记忆量', '释义1', '释义2', '释义3', '释义4', '释义5']]    
    # 添加数据行
    for word, info in database.items():
        row = [word, str(info['count'])] + info['definitions'][:5]  # 保证最多只取五个释义
        row += [''] * (7 - len(row))  # 确保每行都有7个元素
        table_data.append(row)    

    styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue), # 首行的单元格背景颜色
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # 首行的文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # 所有单元格的对齐方式
        ('GRID', (0, 0), (-1, -1), 1, colors.black), # 所有单元格的网格线：黑色，宽度为1
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'), # 使用上面注册的名为Chinese的字体
    ]
    # 创建表格实例
    table = Table(table_data)

    # 指定每列的宽度
    colWidths = [100, 50, 100, 100, 100, 100, 100]  # 根据需要调整  
    # 为所有行设置统一的高度
    rowHeights = [20] * len(table_data)  # 假设每行20点高
    styles.append(('ROWHEIGHTS', (0, 0), (-1, -1), rowHeights)) # 设置每行的高度
    styles.append(('COLWIDTHS', (0, 0), (-1, -1), colWidths)) # 设置每列的宽度))
    
    table.setStyle(TableStyle(styles))

    # 构建PDF文档
    doc.build([table])

    print("PDF文档已生成: wordbook_with_table.pdf")    
    
def generate_random_recite_words(num):
    # 加载JSON文件
    database = load_database()
    
    # 从数据库中随机选择指定数量的单词
    words = list(database.keys())
    random.shuffle(words)
    selected_words = words[:min(num, len(words))]
    word_data = {word: database[word] for word in selected_words}    
    
    # 注册中文字体以支持中文
    pdfmetrics.registerFont(TTFont('Chinese', 'STHeiti Light.ttc'))
    # 创建PDF文档
    doc = SimpleDocTemplate("recitebook_with_table.pdf", pagesize=letter)

    story = []  # 创建一个空的故事列表，用于存放文档内容
    # 获取当前日期并格式化
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 设置样式并创建日期段落
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=CENTER, fontName='Chinese'))
    date_para = Paragraph(current_date, styles['Center'])
    # 将日期段落和一个小的垂直间隔添加到故事中
    story.append(date_para)
    story.append(Spacer(1, 12))  # 添加12点的间隔    
    
    # 准备表格数据
    table_data = [['单词', '记忆量', '释义1', '释义2', '释义3', '释义4', '释义5']]    
    # 添加数据行
    for word, info in word_data.items():
        row = [word, str(info['count'])] + info['definitions'][:5]  # 保证最多只取五个释义
        row += [''] * (7 - len(row))  # 确保每行都有7个元素
        table_data.append(row)    

    styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue), # 首行的单元格背景颜色
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # 首行的文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # 所有单元格的对齐方式
        ('GRID', (0, 0), (-1, -1), 1, colors.black), # 所有单元格的网格线：黑色，宽度为1
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'), # 使用上面注册的名为Chinese的字体
    ]
    # 创建表格实例
    table = Table(table_data)

    # 指定每列的宽度
    colWidths = [100, 50, 100, 100, 100, 100, 100]  # 根据需要调整  
    # 为所有行设置统一的高度
    rowHeights = [20] * len(table_data)  # 假设每行20点高
    styles.append(('ROWHEIGHTS', (0, 0), (-1, -1), rowHeights)) # 设置每行的高度
    styles.append(('COLWIDTHS', (0, 0), (-1, -1), colWidths)) # 设置每列的宽度))
    
    table.setStyle(TableStyle(styles))

    story.append(table)
    # 构建PDF文档
    doc.build(story)

    print("PDF文档已生成: recitebook_with_table.pdf")      

# Example usage
while True:
    word = input("请输入一个单词: ");
    if word.lower() == 'q':
        break
    elif word.lower() == 'g':
        generate_pdf()
    elif word.lower() == 'r':
        generate_random_recite_words(50)
    else:
        add_or_update_word(word)
