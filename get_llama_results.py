from together import Together
from meta import DATASET_FOR_PROMPTING_PTH, PROMPT_FOR_GEN_SUMS, MAX_CONTEXT_LEN, LLAMA_SUMM_FILE_PTH
import pandas as pd
from tqdm import tqdm

def prepare_dataset(df):
    aggregated_texts = df.groupby('case id')['text'].apply(' '.join).to_dict()
    return aggregated_texts

if __name__ == "__main__":
    df = pd.read_excel(DATASET_FOR_PROMPTING_PTH)
    aggregated_texts = prepare_dataset(df)
    results = {}

    client = Together()
    print(len(list(aggregated_texts.keys())))

    for key, val in tqdm(aggregated_texts.items()):
        print(key)
        val = val[:MAX_CONTEXT_LEN]
        stream = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": PROMPT_FOR_GEN_SUMS},
                {"role": "user", "content": val}
            ],
            stream=True,
            )
        
        summary = ""
        for chunk in stream:
            # print(chunk.choices)
            # summary += chunk.choices[0].delta.content or ""

            try:
                if chunk.choices and len(chunk.choices) > 0:
                    summary += chunk.choices[0].delta.content or ""
                else:
                    print("Warning: chunk.choices is empty or None.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        # Save the summarized result to a dictionary
        results[key] = summary

    # Convert the summarized results dictionary to a DataFrame
    summarized_df = pd.DataFrame(list(results.items()), columns=['case_id', 'md_sum'])
    
    # get the case_summary from the original df, and add it to the summarized_df
    df = df.drop_duplicates(subset=['case id'])[['case id', 'case_summary']]
    summarized_df = summarized_df.merge(df[['case id', 'case_summary']], left_on='case_id', right_on='case id', how='left')

    # rename the column
    summarized_df['gt_sum'] = summarized_df['case_summary']
    # drop the columns
    summarized_df.drop(columns=['case id', 'case_summary'], inplace=True)
    # Save the DataFrame to an Excel file
    summarized_df.to_excel(LLAMA_SUMM_FILE_PTH, index=False)