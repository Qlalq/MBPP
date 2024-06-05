import json
import re
import math
# import Counter
# import remove_dirty_chars
# import check
# import defaultdict
# import recursive_list_sum
# import get_equal
# import ct
# import eulerian_num
# import itemgetter
import collections
from typing import List, Dict

import threading

class TimeoutException(Exception): pass
#超时判断
def run_with_timeout(func, args=(), kwargs={}, timeout=2):
    result = {'value': None, 'error': None}

    def target():
        try:
            result['value'] = func(*args, **kwargs)
        except Exception as e:
            result['error'] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutException('Timeout')
    if result['error'] is not None:
        raise result['error']

    return result['value']


def evaluate_samples(sample_file: str, problem_file: str, result_file: str) -> bool:
    with open(sample_file, 'r') as f:
        samples = [json.loads(line) for line in f]
    with open(problem_file, 'r') as f:
        problems = [json.loads(line) for line in f]

    problems_dict = {problem['task_id']: problem for problem in problems}

    results = []
    all_passed = True
    for sample in samples:
        task_id = sample['task_id']
        completion = sample['completion']
        problem = problems_dict[task_id]
        tests = problem['test_list']
        test_imports = problem.get('test_imports', [])

        passed = True
        error_message = ''
        globals_dict = {}
        for import_statement in test_imports:
            try:
                exec(import_statement, globals_dict)
            except Exception as e:
                passed = False
                error_message = f'Error in import: {str(e)}'
                all_passed = False
                break

        if not passed:
            continue

        for i, test in enumerate(tests):
            try:
                print(f'Starting test {i+1}')
                run_with_timeout(exec, (completion, globals_dict), timeout=2)
                run_with_timeout(exec, (test, globals_dict), timeout=2)
                print(f'Finished test {i+1}')
            except TimeoutException:
                passed = False
                error_message = f'Test case {i+1} timed out'
                all_passed = False
                break
            except Exception as e:
                passed = False
                error_message = f'Error in test case {i+1}: {str(e)}'
                all_passed = False
                break

        result = {
            'task_id': task_id,
            'passed': passed,
            'error_message': error_message
        }
        results.append(result)
        print(task_id)

    with open(result_file, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    return all_passed

import json

def calculate_passed_ratio(result_file: str) -> float:
    with open(result_file, 'r') as f:
        lines = f.readlines()

    total = len(lines)
    passed_count = 0

    for line in lines:
        result = json.loads(line)
        if result['passed']:
            passed_count += 1

    return passed_count / total if total > 0 else 0


#大模型回答文件、MBPP源文件、要写入的结果文件
evaluate_samples('MBPP_samples.jsonl', 'MBPP.jsonl', 'MBPP_results.jsonl')
# 调用函数，计算并输出Pass@1
print("Pass@1:",calculate_passed_ratio('MBPP_results.jsonl'))
