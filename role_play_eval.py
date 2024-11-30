import pandas as pd
from util import client
from roleplay_eval_prompt import prompt

def role_play_evaluate_summary(gold_summary:str, model_summary: str):
    
    gold_summary = f"### Gold-standard summary: \n {gold_summary}"
    model_summary = f"### Generated summary: \n {model_summary}"
    
    response = client.chat.completions.create(
        model= "gpt-4o", #"gpt-4-32k", # model = "deployment_name".
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": gold_summary},
            {"role": "user", "content": model_summary},
        ]
    )

    print(response.choices[0].message.content)
    
def prompt_sample(path:str = "results/gpt-40/gpt_test_results.xlsx", is_test=True):
    df = pd.read_excel(path)
    print(df.iloc[1])
    gold_summary = df['gt_sum'][1]
    model_summary = df['md_sum'][1]
    role_play_evaluate_summary(gold_summary, model_summary)
    # response_df = prompt_dataframe(df)
    # if is_test:
    #     save_file_path = "results/gpt-40/gpt_test_results.xlsx"
    # else:
    #     save_file_path = "results/gpt-40/gpt_sample_results.xlsx"
    # response_df.to_excel(save_file_path, index=False)
    # print(f"DataFrame saved to {save_file_path}")
    
# role_play_evaluate_summary(gold_summary:str, model_summary: str)
prompt_sample()