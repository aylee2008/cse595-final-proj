# from together import Together
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from meta import DATASET_FOR_PROMPTING_PTH#, PROMPT_FOR_GEN_SUMS, MAX_CONTEXT_LEN, LLAMA_SUMM_FILE_PTH
import pandas as pd
from tqdm import tqdm
import torch, os

legal_led_max_len = 16384
LEGALLED_SUMM_FILE_PTH = 'data/legal-led-16384/legal-led-16384-summarized-results.xlsx'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Device: {device}")


def prepare_dataset(df):
    aggregated_texts = df.groupby('case id')['text'].apply(' '.join).to_dict()
    return aggregated_texts

if __name__ == "__main__":
    df = pd.read_excel(DATASET_FOR_PROMPTING_PTH)
    aggregated_texts = prepare_dataset(df)
    results = {}

    print(len(list(aggregated_texts.keys())))
    
    # LEGAL-LED model
    tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-led-base-16384")  
    model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-led-base-16384").to(device)
    padding = "max_length"

    for key, val in tqdm(aggregated_texts.items()):
        # print(key)
        # val = val[:legal_led_max_len]
        input_tokenized = tokenizer.encode(val, return_tensors='pt',padding=padding,pad_to_max_length=True, max_length=legal_led_max_len,truncation=True).to(device)
        summary_ids = model.generate(input_tokenized,
                                        num_beams=4,
                                        no_repeat_ngram_size=3,
                                        length_penalty=2,
                                        min_length=350,
                                        max_length=legal_led_max_len)
        summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]
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
    # MAKE OUTPUTDIR IF NOT EXISTS
    os.makedirs(os.path.dirname(LEGALLED_SUMM_FILE_PTH), exist_ok=True)
    # Save the DataFrame to an Excel file
    summarized_df.to_excel(LEGALLED_SUMM_FILE_PTH, index=False)