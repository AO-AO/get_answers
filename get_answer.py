#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import urllib
import urllib.request
import pytesseract
import time
from PIL import Image
from bs4 import BeautifulSoup
import tkinter as tk

CUR_PATH = os.getcwd()
SS_PATH = './shot.png'


def get_ss(out_file_path):
    task_ss_cmd = 'screencapture -oR20,150,390,390 ' + SS_PATH
    os.system(task_ss_cmd)
    return out_file_path


def image_ocr(image_path):
    text = pytesseract.image_to_string(Image.open(
        image_path), lang='chi_sim', config='-psm 6')
    return text


def handle_text(text_buf):
    buf_lines = text_buf.split('\n')
    res_lines = []

    for line in buf_lines:
        if line != '':
            line = line.replace(' ', '')
            res_lines.append(line)

    questions = res_lines[:-3]
    ques_num = questions[0][0]
    ques_str = questions[0][2:]
    for line in questions[1:]:
        ques_str = ques_str + line

    answers = {}
    answers['A'] = res_lines[-3]
    answers['B'] = res_lines[-2]
    answers['C'] = res_lines[-1]
    try:
        print("问题: " + ques_str)
        print("备选答案: ")
        print(answers)
    except Exception as e:
        pass
    return ques_num, ques_str, answers


def query_question(question_str):
    bd_url = "http://www.baidu.com/s?wd=" + question_str
    encoded_url = urllib.parse.quote(bd_url, safe='/:?=', encoding='utf-8')
    response = urllib.request.urlopen(encoded_url)
    soup = BeautifulSoup(response, "html.parser")
    datas = [re.sub(u'<[\d\D]*?>', ' ', str(item))
             for item in soup.select('.c-abstract')]
    return datas


def main():
    try:
        # ss_path = SS_PATH
        ss_path = get_ss(SS_PATH)
        text_buf = image_ocr(ss_path)
        print(text_buf)
        ques_num, ques_str, answers = handle_text(text_buf)
        out_put.delete('1.0', tk.END)
        out_put.insert(tk.END, "问题: " + ques_str + '\n')
        out_put.insert(tk.END, "备选答案: \n")
        out_put.insert(tk.END, str(answers) + '\n')
        query_results = query_question(ques_str)
        query_results_str = ''.join(query_results)
        result_record = {}
        for (key, answer) in answers.items():
            result_record[key] = query_results_str.count(answer)
        result_record_items = result_record.items()
        result = sorted(result_record_items,
                        key=lambda x: x[1], reverse=True)
        result_key = result[0][0]
        print(str(ques_num) + "." + "参考答案: " +
              str(result_key) + ": " + str(answers[result_key]))
        out_put.insert(tk.END, str(ques_num) + "." + "参考答案: " +
                       str(result_key) + ": " + str(answers[result_key]))
        out_put.pack()
    except Exception as e:
        print(e)
        time.sleep(1)
        print("Sleep 1 second!")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("么么扎")
    out_put = tk.Text(root, width=100, height=100)
    count = 0
    while True:
        main()
        if count == 0:
            root.mainloop()
            count += 1
