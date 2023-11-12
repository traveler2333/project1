import openai
import os
import json
import time

#这段代码使用OpenAI GPT-3.5-turbo模型生成对输入prompt的聊天响应
# output.json读取并将生成的内容写入jsonl文件。将出错的键值对记录到错误日志文件中
# 并在最后将错误的键值对保存回原始的output.json文件。
API_URL = "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"

openai.api_key = API_URL


def chatgpt(prompt):
    message = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message, temperature=0)
    return response.choices[0].message['content']

with open("prompt.txt", "r", encoding="utf-8") as prompt_file:
        b = prompt_file.read()
with open("prompt2.txt", "r", encoding="utf-8") as prompt_file:
        b2 = prompt_file.read()
def process_kv_pair(content):
    a = content
    input_data = b + a
    input_data2 = b2 + a 
    with open("out.jsonl", "a", encoding='utf-8') as ff:
        response_content2 = chatgpt(input_data2)# 总结
        response_content = chatgpt(input_data)# 分点概括知识点
        ff.write(response_content2+'\n')
        ff.write(response_content)

# 读取并处理output.json中的键值对
with open("output.json", "r", encoding="utf-8") as output_file:
    data = json.load(output_file)

# 打开错误日志文件
with open("error.txt", "w", encoding="utf-8") as error_file:
    for i, kv_pair in enumerate(data, start=1):
        print(i)
        try:
            content = kv_pair.get("content", "")
            process_kv_pair(content)
        except Exception as e:
            # 在错误文件中记录出错的kv对的位置信息
            error_file.write(f"Error in kv pair at index {i}\n")
            # 可以添加其他需要的处理步骤

# 将出错的键值对保存回output.json
filtered_data = [kv_pair for kv_pair in data if kv_pair.get("error")]
with open("output.json", "w") as output_file:
    json.dump(filtered_data, output_file, indent=2)
