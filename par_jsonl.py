#parquet文件转jsonl文件

import pandas as pd
df = pd.read_parquet('test-00000-of-00001.parquet')
jsonl_data = df.to_json(orient='records', lines=True)
with open('MBPP_test.jsonl', 'w') as f:
    f.write(jsonl_data)