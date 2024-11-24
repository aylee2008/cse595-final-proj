import os
from typing import List
from dotenv import load_dotenv
import pandas as pd
import tiktoken

from prompts import EVALUATE_SYS_PROMPT, PROMPT_SYS_PROMPT

load_dotenv()

# # Access the key and endpoint
azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = azure_openai_endpoint,
  api_key=azure_openai_key, 
  api_version="2024-02-01"
)

def format_user_message(case_docs:List):
    message = ""
    for i, doc in enumerate(case_docs):
       message = message + f"### Case Doc {i}: {doc}\n\n"
    return message
        

def truncate_text(text):
    encoder = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoder.encode(text)
    print(len(text))
    print(len(tokens))
    
    max_context_length = 100000
    truncated_text = encoder.decode(tokens[:max_context_length])
    print(len(truncated_text))
    return truncated_text


def evaluate_summary(gold_summary:str, model_summary: str):
    
    gold_summary = f"### Gold Summary: \n {gold_summary}"
    model_summary = f"### Gold Summary: \n {model_summary}"
    
    response = client.chat.completions.create(
        model= "gpt-4o", #"gpt-4-32k", # model = "deployment_name".
        messages=[
            {"role": "system", "content": EVALUATE_SYS_PROMPT},
            {"role": "user", "content": gold_summary},
            {"role": "user", "content": model_summary},
        ]
    )

    print(response.choices[0].message.content)
    
def query_gpt(sys_prompt, user_message: str):
    response = client.chat.completions.create(
        model= "gpt-4o-low", #"gpt-4-32k", # model = "deployment_name".
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "system", "content": user_message},
        ],
    )
    return response.choices[0].message.content
    #return response.choices[0].message.content
    
def prompt_dataframe(df:pd.DataFrame):
    print(df)
    case_ids = df['case id'].unique().tolist()
    gt_summaries = []
    model_summaries = []
    for case_id in case_ids:
        try:
            gt_summary = list(df[df["case id"] == case_id]['case_summary'])[0]
            case_docs = df[df['case id'] == case_id]['text'].tolist()
            user_message = format_user_message(case_docs)
            truncated_user_message = truncate_text(user_message)
            summary = query_gpt(PROMPT_SYS_PROMPT, truncated_user_message)
            gt_summaries.append(gt_summary)
            model_summaries.append(summary)
        except Exception as E:
            print(f"Expection {E} occured")
            continue
            
    response_df = pd.DataFrame({'case_id': case_ids, 'gt_sum': gt_summaries, 'md_sum':model_summaries})
    return response_df

def prompt_sample(path:str = "data\datasetwlink-clearninghouse-sample-final.xlsx", is_test=False):
    df = pd.read_excel(path)
    response_df = prompt_dataframe(df)
    if is_test:
        save_file_path = "results/gpt-40/gpt_test_results.xlsx"
    else:
        save_file_path = "results/gpt-40/gpt_sample_results.xlsx"
    response_df.to_excel(save_file_path, index=False)
    print(f"DataFrame saved to {save_file_path}")
    
if __name__ == "__main__":
    prompt_sample()