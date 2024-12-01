import argparse
import re
import statistics
import pandas as pd
from tqdm import tqdm
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
        ], temperature=0.2
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content
    

def calculate_mean_and_std(accuracies):
    # Filter out None values and convert the list to floats
    valid_accuracies = [float(acc) for acc in accuracies if acc is not None]
    
    if not valid_accuracies:
        return None, None  # Return None if the list is empty
    
    # Calculate mean and standard deviation
    mean = statistics.mean(valid_accuracies)
    std_dev = statistics.stdev(valid_accuracies) if len(valid_accuracies) > 1 else 0
    return mean, std_dev


def extract_accuracies(text):
    pattern = r'\b(\d+(\.\d+)?%)'
    match = re.search(pattern, text)
    if match:
        accuracy = match.group(0)
        return accuracy.rstrip('%')  # Remove '%' if it exists
    return None
    
def prompt_sample(path:str = "results/gpt-40/gpt_test_results.xlsx", is_test=True):
    df = pd.read_excel(path)
    print(df.iloc[1])
    gold_summary = df['gt_sum'][4]
    model_summary = df['md_sum'][4]
    accuracies = []
    for i in range(10):
        
        res = role_play_evaluate_summary(gold_summary, model_summary)
        acc = extract_accuracies(res)
        accuracies.append(acc)
    print(accuracies)
    mean, std_dev = calculate_mean_and_std(accuracies)
    print(f"Mean: {mean}, Standard Deviation: {std_dev}")


def evaluate_samples(model:str):
    test_path = 'results/gpt-40/gpt_test_results.xlsx'#'results\gpt-40\gpt_test_results.xlsx'
    # sample_results_paths = ['results\llama_70b\sample_summarized_results.xlsx', 
    #                  'results\legal-led-16384\legal-led-16384-sample-summarized-results.xlsx', 
    #                  'results\gpt-40\gpt_sample_results.xlsx']
    sample_results_paths = ['results/gpt-40/gpt_sample_results.xlsx', 
                     'results/legal-led-16384/legal-led-16384-sample-summarized-results.xlsx', 
                     'results/llama_70b/sample_summarized_results.xlsx']
    n = 7
    test_df = pd.read_excel(test_path)
    test_case_ids = test_df['case_id'].unique().tolist()
    print(test_case_ids)
    updated_rows = []
    
    # sample_path = ""
    if model == 'gpt-40':
        sample_path = sample_results_paths[0]
    elif model == "llama_70b":
        sample_path = sample_results_paths[2]
    else:
        sample_path = sample_results_paths[1]
    
    # for sample_path in tqdm(sample_results_paths, desc="Processing Models"):
    test_count = 0
    print(model)
    print("Sample path is ")
    print(sample_path)
    model = sample_path.split('/')[1]
    df = pd.read_excel(sample_path)
    # df = df.sample(3,random_state=42)
    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing {model} Samples", leave=False):
        row_dict = row.to_dict()
        
        case_id = row_dict['case_id']
        gold_summary = row_dict['gt_sum']
        model_summary = row_dict['md_sum'] 
        accuracies = []
        
        for i in range(n):
            res = role_play_evaluate_summary(gold_summary, model_summary)
            acc = extract_accuracies(res)
            accuracies.append(acc)
            
        mean, std_dev = calculate_mean_and_std(accuracies)
        is_test = False
        if case_id in test_case_ids:
            test_count += 1
            is_test = True
        row_dict['model'] = model
        row_dict['is_test'] = is_test
        row_dict['accuracies'] = str(accuracies)
        row_dict['mean_acc'] = mean
        row_dict['std'] = std_dev
        updated_rows.append(row_dict)
        print(f"Test count for model: {model} is {test_count}")
    updated_df = pd.DataFrame(updated_rows)
    print(f"Update df len is {len(updated_df)}")
    save_file_path = f"results/{model}evalution_results.xlsx"
    updated_df.to_excel(save_file_path, index=False)
    print(f"DataFrame saved to {save_file_path}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a model.")
    parser.add_argument('--model', type=str, required=True, help="model to process")
    args = parser.parse_args()
    
    evaluate_samples(args.model)