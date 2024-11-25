CASE_ID_COL = "case id"
COMPLAINT_CNT_COL = "complaint count"
APPEAL_CNT_COL = "appeal count"
DOCKET_CNT_COL = "docket count"
RESULT_CASE_TYPES_COL = "case types"

DATASET_PTH = 'data/DatasetWLink-ClearningHouse-cnt-no-none.xlsx'
DATASET_OUT_PTH = 'data/DatasetWLink-ClearningHouse-cnt-no-none-cnt.xlsx'
#DATASET_FOR_PROMPTING_PTH = 'data/datasetwlink-clearninghouse-test-final.xlsx'
DATASET_FOR_PROMPTING_PTH = 'data/datasetwlink-clearninghouse-sample-final.xlsx'
# LLAMA_SUMM_FILE_PTH = 'data/llama_70b/test_summarized_results.xlsx'
LLAMA_SUMM_FILE_PTH = 'data/llama_70b/sample_summarized_results.xlsx'

MAX_CONTEXT_LEN = 131072

PROMPT_FOR_GEN_SUMS = '''
Your task is to summarize multiple legal case documents. Follow these rules carefully to create a summary:

### Writing Style and Structure:
1. Write in clear, accessible language while maintaining legal precision.
2. The summary should consist of **four to twelve paragraphs**.
3. Begin the summary with a sentence that captures the overall topic of the case.
4. Conclude the summary with a **one-sentence statement** about the current status of the case.

### Required Information:
#### First Paragraph:
5. Provide the following details in the first paragraph:
   - Provide the **Date** the complaint was filed.
   - If the plaintiff is an organization, state its **name**; if the plaintiff is an individual, describe them without naming.
   - List the **defendant(s)**.
   - Specify the **full name of the court** handling the case.
   - Identify the **full name and title of the judge** presiding.
   - State the **cause of action** (e.g., statutory, constitutional, or other legal grounds).
   - For constitutional claims, include the relevant **amendment** and **clause**.
   - Describe the **requested relief**, including attorneys’ fees if applicable.
   - Mention the **attorney organizations** representing the plaintiffs.
   
#### Factual Background:
6. Provide a concise description of the facts alleged in the **complaint**.

#### Court Opinions and Legal Reasoning:
7. Summarize the **legal reasoning** of every court opinion. Each description should be at least **three sentences long**.

#### Dates for Orders, Motions, and Key Events:
8. Include and provide the **dates** for any orders or motions related to:
   - Dismissal
   - Summary judgment
   - Class certification (state the conclusion only, without the reasoning)
   - Settlement
   - Consent decrees
   - Attorneys’ fees
   - Consolidation
   - Injunctions
   - Temporary restraining orders
   - Intervention
   - Enforcement of a settlement agreement
9. If applicable, summarize and provide the **date** for:
   - Report and recommendation
   - Amended complaint (highlight differences from the original)
   - Statement of interest
   - Opinion on rehearing en banc
   - Trial
   - Settlement agreement
   - Consent decree
   - Appeal

#### Specific Details to Include:
10. If the case involves an appeal, state the **full name of the appellate court**.
11. If the case is a class action, describe the **class** and any **subclasses**.
12. For constitutional claims against state or local government officials, state that the cause of action is **42 USC Section 1983**.
13. If a settlement agreement or consent decree exists, summarize its **substantive terms**, including:
    - Monitoring mechanisms
    - Policy changes
    - Monetary payments
    - Duration of enforceability

#### Exclusions:
14. Do not include information about **protective orders**, **motions to compel**, **motions to seal**, or **discovery disputes**.

#### Style:
15. Refer to the plaintiffs as “plaintiff(s)” rather than by name.
16. Use plain paragraphs only—do not use any additional formatting such as headings, lists, or numbered sections.
'''