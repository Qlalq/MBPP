# usage
## format conversion
Given the network issues, the tutorial here requires the MBPP dataset on Huggingface to be downloaded. I have already downloaded it, it is **test-00000-of-00001.parquet**. the download address is below:
>https://huggingface.co/datasets/google-research-datasets/mbpp/tree/main/sanitized
In order to adapt to the now mainstream jsonl representation (since I won't be using parquet (つω`.)), you need to convert parquet to jsonl

The conversion file is **par_jsonl.py** and the result of the **test-00000-of-00001.parquet** conversion is **MBPP.jsonl**
## Answer Generation
Call the API to evaluate the LLM (you need to fill in the **API_key** before that)
``python MBPP_completion.py``
The sample result is **MBPP_samples.jsonl**
## Evaluation of results
Run the python code on your own system and calculate Pass@1
``python evaluate_MBPP.py``
The generated result is **MBPP_results.jsonl**
## Sample Error Summary
Error cases are summarized in **failed_tasks.txt**