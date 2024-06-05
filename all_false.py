"""我希望将错误用例单独列出来，具体操作如下：
找出MBPP_results.jsonl中"passed": false的"task_id"
根据"task_id"找出对应的"prompt"（MBPP.jsonl里）和"completion"(MBPP_samples.jsonl里)和"error_message"（MBPP_results.jsonl里）
并将这四个放在一起写入一个txt文件中
"""
import json

# 读取MBPP_results.jsonl文件，找出所有"passed": false的"task_id"
with open('MBPP_results.jsonl', 'r') as file:
    failed_tasks = [json.loads(line)['task_id'] for line in file if json.loads(line)['passed'] is False]

# 读取MBPP.jsonl和MBPP_samples.jsonl文件，找出对应的"prompt"和"completion"
prompts = {}
task_list = {}
completions = {}
with open('MBPP.jsonl', 'r') as file:
    prompts = {json.loads(line)['task_id']: json.loads(line)['prompt'] for line in file if json.loads(line)['task_id'] in failed_tasks}
    task_list={json.loads(line)['task_id']: json.loads(line)['test_list'] for line in file}
with open('MBPP_samples.jsonl', 'r') as file:
    completions = {json.loads(line)['task_id']: json.loads(line)['completion'] for line in file if json.loads(line)['task_id'] in failed_tasks}

# 从MBPP_results.jsonl中找出对应的"error_message"
error_messages = {}
with open('MBPP_results.jsonl', 'r') as file:
    error_messages = {json.loads(line)['task_id']: json.loads(line)['error_message'] for line in file if json.loads(line)['task_id'] in failed_tasks}

# 将这四个信息放在一起，写入一个txt文件中
with open('failed_tasks.txt', 'w') as file:
    for task_id in failed_tasks:
        file.write(f'Task ID: {task_id}\n')
        file.write(f'Prompt: {prompts[task_id]}\n')
        file.write(f'Completion: {completions[task_id]}\n')
        if task_id in task_list:
            file.write(f'Test List: {task_list[task_id]}\n')
        file.write(f'Error Message: {error_messages[task_id]}\n\n')
        file.write('----------------------------------------\n\n')