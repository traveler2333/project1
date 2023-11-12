from docx import Document
import os
import re
import json
# 这是一个可以将word文档中的章节内容分割成小节的脚本

content_dict_list = []
doc_path = r"D:\aaa_code\python\project\新城市科学概论-修改（clean）.docx"
output_path = r"D:\aaa_code\python\myself"


def split_document_by_chapter(doc_path):
    doc = Document(doc_path)
    chapter_texts = []

    current_chapter = ""
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text.startswith("第") and "章：" in text:
            if current_chapter:
                # 删除参考文献后的内容
                current_chapter = delete_references(current_chapter)
                chapter_texts.append(current_chapter)
            current_chapter = text
        else:
            current_chapter += " " + text

    # 添加最后一个章节
    if current_chapter:
        # 删除参考文献后的内容
        current_chapter = delete_references(current_chapter)
        current_chapter = remove_figure_references(current_chapter)
        chapter_texts.append(current_chapter)

    return chapter_texts


def delete_references(chapter_text):
    # 在这里根据具体的文档格式删除参考文献后的内容
    # 这里简单示范一个删除所有内容的方法
    references_index = chapter_text.find("参考文献")
    if references_index != -1:
        chapter_text = chapter_text[:references_index]

    return chapter_text


# 指定文档路径


def split_by_section(chapter_text, idx):
    pattern = re.compile(r"\s+(?={}\.\d+\s+(?!\.))".format(idx))
    sections = pattern.split(chapter_text)
    sections = [s.strip() for s in sections if s.strip()]
    return sections


def split_by_subsection(section_text, idx):
    pattern = re.compile(r"(?={}\.\d+\.\d+\s+)".format(idx))
    subsections = pattern.split(section_text)
    subsections = [s.strip() for s in subsections if s.strip()]
    return subsections


def remove_figure_references(text):
    text = re.sub(r"（图\s*\d+-\d+）", "", text)
    return text


def get_section_title(section_content):
    print()
    pattern = r'(?<!\.)\d+\.\d\s+([\S]+)'
    match = re.search(pattern, section_content)
    if match:
        return match.group(1)
    return "空"


def get_subsection_title(subsection_content):
    match = re.search(r"\d+\.\d+\.\d+\s+([\S]+)", subsection_content)
    if match:
        return match.group(1)
    return "空"


chapter_texts = split_document_by_chapter(doc_path)


def find_sentence_after_chapter(chapter_text):
    pattern = r'第\d+章[^第\s]+'
    match = re.search(pattern, chapter_text)
    if match:
        return match.group()
    return ""


# 长度微调



# 继续处理章节内容
# 继续处理章节内容
for idx, chapter_text in enumerate(chapter_texts):
    # 提取段落标题
    title = find_sentence_after_chapter(chapter_text)
    # 用一级标题分割章节内容
    print("title是:" + title)
    firsts = split_by_section(chapter_text, idx)
    if (idx == 3):
        title += " 第四次工业革命与新城市科学"
    # 第一小节直接用章节标题，产生kv对
    if len(firsts[0]) < 500 and len(firsts[0]) > 50:
        # 如果title为空，使用“书籍大纲总结”
        if title == "":
            title = "书籍大纲总结"
        content_dict_list.append({"title": title, "content": firsts[0]}) # 保存到字典中
    # 从第二小节开始
    for chapter2 in firsts[1:]:
        # 用二级标题分割章节内容
        title1 = title + ' ' + get_section_title(chapter2) + ' '
        print("title1是:" + title1)
        seconds = split_by_subsection(chapter2, idx)
        if len(seconds[0]) < 500 and len(seconds[0]) > 50:
            content_dict_list.append({"title": title1, "content": seconds[0]})

        # 从第三小节开始
        for chapter3 in seconds[1:]:
            # 用三级标题分割章节内容
            title2 = title1 + get_subsection_title(chapter3)
            print("title2是:" + title2)
            if len(chapter3) < 500 and len(chapter3) > 50:
                content_dict_list.append({"title": title2, "content": chapter3})

# 将结果保存到JSON文件中
if content_dict_list:
    output_json_path = os.path.join(output_path, "output.json")
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(content_dict_list, json_file, ensure_ascii=False, indent=2)
