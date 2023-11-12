import json
#这是一个处理jsonl文件的代码，将jsonl文件中的每一行转换为一个json对象
#然后将其写入到一个新的jsonl文件中，根据 'title' 字段去除重复条目，并将唯一的条目写入新的 jsonl 文件。


input_file_path = 'out.jsonl'
output_file_path = 'processed_out.jsonl'


with open(input_file_path, 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in lines:
        
        cleaned_line = line.strip()

        
        if not cleaned_line:
            continue

        objects = cleaned_line.split('}{')

        # Write each JSON object as a separate line
        for obj in objects:
            # Handle the leading or trailing '{' or '}' if necessary
            obj = obj.strip('{}')

            try:
                # Load JSON from the cleaned line
                json_data = json.loads('{' + obj + '}')

                # Write the whole JSON object as a separate line
                output_file.write(json.dumps(json_data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Problematic line: {line}")

# Input and output file paths
input_file_path = 'processed_out.jsonl'
output_file_path = 'final_output.jsonl'

# Dictionary to store unique titles and their corresponding objects
title_dict = {}

# Read data from the input file
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Write cleaned data to the output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in lines:
        # Remove leading and trailing whitespaces
        cleaned_line = line.strip()

        # Skip empty lines
        if not cleaned_line:
            continue

        try:
            # Load JSON from the cleaned line
            json_data = json.loads(cleaned_line)

            # Extract title and content
            title = json_data.get('title')
            content = json_data.get('content', '')

            # Check for duplicate titles
            if title in title_dict:
                # Compare content lengths and keep the longer one
                existing_content = title_dict[title].get('content', '')
                if len(content) > len(existing_content):
                    title_dict[title] = json_data
            else:
                title_dict[title] = json_data

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic line: {line}")

    # Write unique data to the output file
    for title_data in title_dict.values():
        output_file.write(json.dumps(title_data, ensure_ascii=False) + '\n')


        
#这是一个处理jsonl文件的代码，将jsonl文件中的每一行转换为一个json对象，然后将其写入到一个新的json文件中

# Input and output file paths
input_file_path = 'final_output.jsonl'
output_file_path = 'out.json'

# List to store JSON objects
json_objects = []

# Read data from the input file
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Parse each line and append to the list
for line in lines:
    cleaned_line = line.strip()
    if cleaned_line:
        try:
            json_data = json.loads(cleaned_line)
            json_objects.append(json_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic line: {line}")

# Write the list of JSON objects to the output file as a JSON array
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(json_objects, output_file, ensure_ascii=False, indent=2)

import json

#这段代码读取一个JSON文件，过滤掉其中'title'字段为空的JSON对象。
#然后将过滤后的JSON对象写入到同一个文件中

# Input and output file paths
input_file_path = 'out.json'

# List to store filtered JSON objects
filtered_json_objects = []

# Read data from the input file
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    json_objects = json.load(input_file)

# Filter out objects with non-empty 'title'
filtered_json_objects = [obj for obj in json_objects if obj.get('title')]

# Write the filtered list of JSON objects to the output file
with open(input_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(filtered_json_objects, output_file, ensure_ascii=False, indent=2)


#将这两个 JSON 对象列表合并成一个列表。
#然后将合并的列表写入新的文件。

# Input file paths
out_file_path = 'out.json'
filtered_output_file_path = 'filtered_output.json'#长度小于500的，在finish.py中设置

# Output file path
merged_output_file_path = 'merged_output.json'

# List to store merged JSON objects
merged_json_objects = []

# Read data from out.json
with open(out_file_path, 'r', encoding='utf-8') as out_file:
    out_json_objects = json.load(out_file)
    merged_json_objects.extend(out_json_objects)

# Read data from filtered_output.json
with open(filtered_output_file_path, 'r', encoding='utf-8') as filtered_output_file:
    filtered_json_objects = json.load(filtered_output_file)
    merged_json_objects.extend(filtered_json_objects)

# Write the merged list of JSON objects to the output file
with open(merged_output_file_path, 'w', encoding='utf-8') as merged_output_file:
    json.dump(merged_json_objects, merged_output_file, ensure_ascii=False, indent=2)



#这段代码合并了一个包含JSON对象的文件，然后根据每个对象的 'title' 字段去除重复
# 并保留每个 'title' 对应内容较长的对象。最后，将唯一的 JSON 对象列表写入新的文件。

# Input and output file paths
merged_output_file_path = 'merged_output.json'
final_output_file_path = 'final_merged_output.json'

# Dictionary to store unique titles and their corresponding objects
title_dict = {}

# Read data from the merged output file
with open(merged_output_file_path, 'r', encoding='utf-8') as merged_output_file:
    merged_json_objects = json.load(merged_output_file)

# Check for duplicate titles and keep the longer content
for json_data in merged_json_objects:
    title = json_data.get('title')
    content = json_data.get('content', '')

    if title in title_dict:
        existing_content = title_dict[title].get('content', '')
        if len(content) > len(existing_content):
            title_dict[title] = json_data
    else:
        title_dict[title] = json_data

# Write unique data to the final output file
with open(final_output_file_path, 'w', encoding='utf-8') as final_output_file:
    json.dump(list(title_dict.values()), final_output_file, ensure_ascii=False, indent=2)
    


#这是去重的代码，将两个json文件中的内容合并到一个新的json文件中
# Input file paths
final_out_file_path = 'final_merged_output.json.json'#自动处理的
output_2_file_path = 'output(2).json'#手动处理的

# Output file path
merged_final_output_file_path = 'final_output1.json'

# Dictionary to store unique titles and their corresponding objects
title_dict = {}

# Read data from final_out.json
with open(final_out_file_path, 'r', encoding='utf-8') as final_out_file:
    final_out_json_objects = json.load(final_out_file)
    for json_data in final_out_json_objects:
        title = json_data.get('title')
        title_dict[title] = json_data

# Read data from output(2).json
with open(output_2_file_path, 'r', encoding='utf-8') as output_2_file:
    output_2_json_objects = json.load(output_2_file)
    for json_data in output_2_json_objects:
        title = json_data.get('title')
        # Only add to title_dict if title doesn't exist
        if title not in title_dict:
            title_dict[title] = json_data

# Write the merged list of JSON objects to the output file
with open(merged_final_output_file_path, 'w', encoding='utf-8') as merged_final_output_file:
    json.dump(list(title_dict.values()), merged_final_output_file, ensure_ascii=False, indent=2)
