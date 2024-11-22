import pandas as pd
import numpy as np

def process_data(crawl_file_path: str = "data\datasetwlink-clearninghouse-cnt-final.xlsx", main_file_path:str = "data\DatasetWLink-ClearningHouse.xlsx") -> pd.DataFrame:

  df = pd.read_excel(crawl_file_path)
  main_df = pd.read_excel(main_file_path)

  # process main_df
  main_df.rename({"列1":"case id", "列2": "document length"}, inplace=True, axis=1) # rename columns

  # drop nan row on doc_id, convert count columns to ints
  main_df = main_df[main_df['doc_id'].notna()]
  float_cols = main_df.select_dtypes(include='float').columns
  main_df[float_cols] = main_df[float_cols].astype(int)

  aggregated = main_df.groupby('case id').agg(
      doc_count=('doc_id', 'count'),
      doc_len_sum=('document length', 'sum')
      ).reset_index()

  final_df = df.merge(aggregated, on='case id', how='left')
  df = final_df.copy()
  return df, main_df
  
def calculate_difficulty(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['difficulty'] = (df['doc_len_sum'] * 0.333) + (df['appeal count'] * 0.167) + (df['docket count'] * 0.228) + (df['complaint count'] * 0.167) + (df['appeal count'] * 0.222)

    # Normalize the score
    df['difficulty'] = (df['difficulty'] - df['difficulty'].min()) / (df['difficulty'].max() - df['difficulty'].min())

    # Create difficulty category based on normalized score
    conditions = [
        (df['difficulty'] < 0.33),  # Easy cases
        (df['difficulty'] >= 0.33) & (df['difficulty'] < 0.66),  # Medium cases
        (df['difficulty'] >= 0.66)  # Hard cases
    ]
    choices = ['Easy', 'Medium', 'Hard']
    df['case_difficulty'] = np.select(conditions, choices, default='Unknown')
    print(df['case_difficulty'].value_counts())

    return df

  

def filter_data_based_on_difficulty(df_with_difficulty: pd.DataFrame, n: int = 6, random_state=42) -> pd.DataFrame:
    #make sure n is divisible by 3
    if n%3 != 0:
      raise ValueError("n must be divisible by 3")
    num_per_group = n // 3
    
    # select hardest and easiest questions
    hardest_cases = df_with_difficulty.nlargest(num_per_group, 'difficulty')  # Top 2 hardest cases (largest difficulty)
    easiest_cases = df_with_difficulty.nsmallest(num_per_group, 'difficulty')  # Top 2 easiest cases (smallest difficulty)
    
    # Filter medium difficulty cases 
    medium_cases = df_with_difficulty[df_with_difficulty['case_difficulty'] == 'Medium']
    
    # Randomly select 2 medium difficulty cases
    medium_cases_random = medium_cases.sample(n=num_per_group, random_state=random_state)

    # Concatenate the selected cases
    selected_data = pd.concat([hardest_cases, easiest_cases, medium_cases_random], ignore_index=True)
    
    return selected_data

def sample_data(df: pd.DataFrame, random_state: int = 42, sample_size = 100):
    # Step 1: Define thresholds and create categories
    df['doc_len_category'] = pd.qcut(df['doc_len_sum'], q=[0, 0.25, 0.75, 1], labels=['Short', 'Medium', 'Long'])
    df['doc_count_category'] = np.where(df['doc_count'] > 10, 'Large', 'Small')
    df['docket_count_category'] = np.where(df['docket count'] > 200, 'Large', 'Small')
    df['appeal_count_category'] = np.where(df['appeal count'] > 2, 'Large', 'Small')
    df['complaint_count_category'] = np.where(df['complaint count'] > 2, 'Large', 'Small')

        # # Define proportions for doc length
    proportions = {'Short': 0.25, 'Medium': 0.50, 'Long': 0.75}

    # Final sample
    random_state = 42
    offset = 20
    final_sample = pd.DataFrame()

    # Loop through each case type
    for case_type in df['case types'].unique():
        case_type_group = df[df['case types'] == case_type]
        
        for length in ['Short', 'Medium', 'Long']:
            # Filter by doc length
            length_group = case_type_group[case_type_group['doc_len_category'] == length]
            
            # Apply nested filtering rules
            large_docs = length_group[length_group['doc_count_category'] == 'Large']
            small_docs = length_group[length_group['doc_count_category'] == 'Small']
            large_dockets = length_group[length_group['docket_count_category'] == 'Large']
            small_dockets = length_group[length_group['docket_count_category'] == 'Small']
            large_appeals = length_group[length_group['appeal_count_category'] == 'Large']
            small_appeals = length_group[length_group['appeal_count_category'] == 'Small']
            large_complaints = length_group[length_group['complaint_count_category'] == 'Large']
            small_complaints = length_group[length_group['complaint_count_category'] == 'Small']
            
            # Sample within each rule category for diversity
            sampled_data = pd.concat([
                large_docs.sample(frac=0.1, random_state=random_state, replace=True),
                small_docs.sample(frac=0.1, random_state=random_state, replace=True),
                large_dockets.sample(frac=0.1, random_state=random_state, replace=True),
                small_dockets.sample(frac=0.1, random_state=random_state, replace=True),
                large_appeals.sample(frac=0.1, random_state=random_state, replace=True),
                small_appeals.sample(frac=0.1, random_state=random_state, replace=True),
                large_complaints.sample(frac=0.1, random_state=random_state, replace=True),
                small_complaints.sample(frac=0.1, random_state=random_state, replace=True),
            ])
            
            # Ensure proportionality based on doc length category
            sampled_data = sampled_data.sample(frac=proportions[length], random_state=random_state, replace=True)
            
            # Add to final sample
            final_sample = pd.concat([final_sample, sampled_data])

    if final_sample.shape[0] <= sample_size:
        return final_sample
    
    # select sample size
    final_sample = final_sample.sample(n=sample_size+offset, random_state=random_state)

    # Make sure extreme conditions are included in the sample 
    filtered_complaints = df[df['complaint count'] >= 7]
    filtered_appeals = df[df['appeal count'] >= 30]
    filtered_docket = df[df['docket count'] == 12177]
    filtered_docs = df[df['doc_count'] >= 100]

    filtered_data = pd.concat([filtered_complaints, filtered_appeals, filtered_docket, filtered_docs])
    print(filtered_data.shape)

    # Append the filtered rows to the final sample (final_sample)
    final_sample = pd.concat([final_sample, filtered_complaints, filtered_appeals, filtered_docket, filtered_docs], ignore_index=True)

    # Verify the final DataFrame
    print(final_sample.shape)
    # Drop duplicates if any were added due to replacements
    final_sample = final_sample.drop_duplicates()
    return df, final_sample

def sample_test_split(df:pd.DataFrame, sample_df: pd.DataFrame, test_size:int =6):
    # Select rows from main_df where case_id is present in sample_df
    filtered_main_df = df[df['case id'].isin(sample_df['case id'])]
    test_df = filter_data_based_on_difficulty(sample_df, n = test_size, random_state=42)
    test_df = filtered_main_df[filtered_main_df['case id'].isin(test_df['case id'])]

    filtered_main_df = filtered_main_df.merge(sample_df, on='case id', how='left')
    test_df = test_df.merge(sample_df, on='case id', how='left')
    
    return filtered_main_df, test_df 

def main():
    df, main_df = process_data()
    df = calculate_difficulty(df)
    df, final_sample = sample_data(df)
    filtered_main_df, test_df = sample_test_split(main_df, final_sample, test_size=6)
    
    print(f"Test Size for human evalution is {test_df['case id'].nunique()}")
    print(f"Sample Size for is {filtered_main_df['case id'].nunique()}")


    # Save DataFrame to Excel
    sample_file_path = "data/datasetwlink-clearninghouse-sample-final.xlsx"
    test_file_path = "data/datasetwlink-clearninghouse-test-final.xlsx"
    filtered_main_df.to_excel(sample_file_path, index=False)
    test_df.to_excel(test_file_path, index=False)

    print(f"DataFrame saved to {sample_file_path} and {test_file_path}")
    
if __name__ == "__main__":
    main()