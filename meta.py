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

# prompt for evaluation using a single llm model - adapted from Chima's original version
PROMPT_FOR_EVAL_SINGLE = r"""

You are an evaluator for a legal multi-document summarization task. Evaluate the given model summary of a legal case based on the reference ("Ground Truth Summary") using the checklist below. Follow the instructions and return the evaluation form with scores. Use the "Aggregate" column to determine the final score. For items not present in the "Ground Truth Summary," ignore the other columns. Ensure the output strictly adheres to the provided format. 

---

### Evaluation Checklist
For each checklist(question) item:  
1. **Answer in Ground Truth Summary**: **yes** or **no**.
   If **no**, skip the other columns for this item.  
   Some questions may not be applicable to the summary (e.g. the summary does not contain the information, but the question asks about it). In such cases, the answer is **no**.
2. **Answer in Model Summary**: **yes** or **no**.  
   Some questions may not be applicable to the summary (e.g. the summary does not contain the information, but the question asks about it). In such cases, the answer is **no**.
3. **Aggregate**: This is `1` only if all the following conditions are true otherwise '0':   
   - **Answer in Ground Truth Summary** = **yes**  
   - **Answer in Model Summary** = **yes**

---

### Instructions
1. Review the "Ground Truth Summary" and "Model Summary."
2. For each checklist item:  
   - Mark **Answer in Ground Truth Summary** as `yes` or `no`.  
   - If "Answer in Ground Truth Summary" = `no`, skip the rest of the columns for that row.  
   - Otherwise, evaluate "Answer in Model Summary"
   - Compute the "Aggregate" column.  
3. Calculate the **Final Score** as:  
   - \( \text{Final Score (\%)} = \left( \frac{\text{Sum of Aggregate Scores}}{\text{Total Items with Answer in Ground Truth Summary = yes}} \right) \times 100 \).  

---

### Input
**Ground Truth Summary:**  
{{}}  
**Model Summary:**  
{{}}

---

### Checklist items
1. **Filing Date**
   - Filing Date - 1: Whether it contains the Date: yes/no
   - Filing Date - 2: Whether the Date is correct (compare with the reference): yes/no
      - yes: the summary contains consistent and correct dates;
      - no: some or all filling date information is incorrect

2. **Plaintiff Type**
   If there are class action plaintiffs the summary should say it's a class action; if there are individual plaintiffs it can just describe the plaintiffs. For example, use specific terms like "The city" or "The parents" rather than general terms like "The defendant" or "The plaintiffs."
   - Plaintiff Type - 1: Whether it contains the information: yes/no
      - yes: the summary clearly states the plaintiff information
      - no: do not mention whether it’s a class action or individual plaintiffs
   - Plaintiff Type - 2: Whether the detailed information is correct: if there are class action plaintiffs the summary should say it's a class action; if there are individual plaintiffs the summary can just describe the plaintiffs (same with the reference): yes/no
      - yes: the summary consistently and correctly states whether it is a Class Action or Individual Plaintiffs (describe the plaintiffs).
      - no: the summary does not consistently and correctly state whether it is a Class Action or Individual Plaintiffs (describe the plaintiffs).

3. **Cause of Action**
   eg. a statute (e.g. 42 USC 1983) or a case (e.g. Ex Parte Young)
   - Cause of Action - 1: Whether it contains the information: yes/no
      - yes: the summary clearly states the action information
      - no: do not mention the action information
   - Cause of Action - 2: Whether the detailed information is correct: what is the action type? What is the action set? (same with the reference): yes/no 
      - yes: the summary consistently and correctly states the type of action
      - no: mention the wrong action information

4. **Statutory or Constitutional Basis for the Case**
   A case can either be based on a statute or a provision of the Constitution--i.e., a case will either claim that someone violated a statute, or violated the Constitution. For cases that have a constitutional basis, the summary should refer to the clause of the Constitution that was allegedly violated, as well as the amendment if applicable. So for example it would say "the plaintiffs alleged violations of the Fourteenth Amendment's Equal Protection Clause," or "the plaintiffs alleged violations of the Commerce Clause."
   - Statutory Basis for Case - 1: Whether it claim that someone violated a statute or violated the Constitution: yes, no
   - Statutory Basis for Case - 2: Whether it contains the statutory bases information or constitutional bases information: yes/no
      - yes: contains the statutory bases or constitutional bases information
      - no: do not contain any statutory basis or constitutional bases information
   - Statutory Basis for Case - 3: Whether the detailed information is correct: what are the statutory bases? (same with the reference): yes/no
      - yes: contains all the right statutory bases
      - no: do not contains all the right statutory bases

5. **Remedy Sought**
   eg. declaratory judgment
   - Remedy Sought - 1: Whether it contains the information: yes/no
   - Remedy Sought - 2: Whether the detail information is correct: (same with the reference): yes/no

6. **Who are the parties**
   description, not name
   - Who are the parties - 1: Whether it contains both the plaintiff and description of the defendants information: yes/no
      - Whether it contains the plaintiff information
      - Whether it contains the  description of the defendants (usually based on their office/position if it's a government official)
   - Who are the parties - 2: Whether the detail information is correct: (same with the reference)
      - Is the plaintiff correct? yes/no
      - Is the defendant correct? yes/no

7. **Note important filings (if applicable)**
   Note important filings including motions for temporary restraining orders or preliminary injunctions, motions to dismiss, motions for summary judgment, etc.
   - Note important filings (if applicable) - 1: Whether it contains the information: yes/no
   - Note important filings (if applicable) - 2: Whether the detail information is correct: (same with the reference)
      - Are the types of filings correct? yes/no

8. **Significant Terms of decrees (if applicable)**
   Significant terms means the substance of the decree or settlement. In a decree, the judge orders the defendants to do something; in a settlement, the defendants agree to do something. The significant terms would just be what the defendants are ordered/agree to do. Here are some examples that indicate how much detail is required:
   Adams & Knights v. Kentucky 3:14-cv-00001 (E.D. Ky.) | Civil Rights Litigation Clearinghouse
   The parties reached a settlement, which the court approved on June 24, 2015. The settlement required KDOC to do the following:
   ensure full and equal access to all services and accommodations;
   assign a staff member at each KDOC adult institution as an ADA coordinator;
   provide during initial intake effective communication, hearing assessment, and auxiliary aids and services in the form of qualified interpreters, etc.;
   ensure staff awareness through identification cards;
   provide deaf inmates with the interpretation of materials;
   provide deaf inmates with a schedule showing when interpretation services are available;
   ensure deaf and hard of hearing inmates get equal access to on-site and off-site medical care, various programs, work assignments, religious services, and any meetings relating to transfer and classification matters;
   provide interpretation for disciplinary proceedings, announcements, alarms, and any other information audibly conveyed to the inmates;
   provide telecommunication devices and other adequate technology devices; and
   train KDOC employees on the implementation of new policies.
   The settlement was scheduled to last 5 years and provided for the appointment of a monitor, Margo Schlanger.
   EEOC v. Walmart 6:20-cv-00163 (E.D. Ky.) | Civil Rights Litigation Clearinghouse
   The consent decree applied to all Walmart grocery distribution centers. The decree provided injunctive relief, including requiring Walmart to cease use and refrain from using for five years a physical abilities test for hiring order fillers at grocery distribution centers. Walmart was also forbidden from engaging in employment practices that discriminate on the basis of sex and from engaging in employment practices that discriminate on the basis of involvement in the EEOC proceedings, the proceedings on the claim against Walmart, or any other proceeding under Title VII.
   The consent decree also provided significant monetary relief. The decree ordered Walmart to pay $20,000,000.00 into a Qualified Settlement Fund as part of the resolution, to be distributed to eligible claimants at the sole discretion of the EEOC. Eligible claimants include women who applied for the position of orderfiller at a Walmart grocery distribution center between February 1, 2020 and the time Walmart ceased use of the physical abilities test and who did not score competitively on the physical abilities test, and therefore did not move forward in the hiring process for the position of orderfiller. The decree also shifts the costs of a claims administrator up to $250,000.00 to Walmart, allowing a mutually agreed upon claims administrator to oversee the claims process and payments to eligible claimants. The consent decree also awarded the EEOC costs for the action.
   Further, the consent decree mandated certain training and notification requirements. The decree required Walmart to provide training to employees who have hiring or supervisory responsibilities for grocery orderfillers regarding the terms of the consent decree including the cessation of the physical abilities test, clear and accurate information about the grocery orderfiller job requirements and qualifications, and information on what constitutes unlawful employment practice under Title VII. Walmart was also required to certify compliance with certain aspects of the consent decree in writing to the EEOC.
   - Significant Terms of decrees (if applicable) - 1: Whether it contains details about the significant terms: yes/no
   - Significant Terms of decrees (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

9. **Dates of all decrees (if applicable)**
   - Dates of all decrees (if applicable) - 1: Whether it contains the information: yes/no
   - Dates of all decrees (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

10. **How long decrees will last (if applicable)**
   - How long decrees will last (if applicable) - 1: Whether it contains the information: yes/no
   - How long decrees will last (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

11. **Significant Terms of settlement (if applicable)**
   - Significant Terms of settlement (if applicable) - 1: Whether it contains details about the significant terms: yes/no
   - Significant Terms of settlement (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

12. **Date of settlement (if applicable)**
   - Date of settlement (if applicable) - 1: Whether it contains the information: yes/no
   - Date of settlement (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

13. **How long settlement will last (if applicable)**
   - How long settlement will last (if applicable) - 1: Whether it contains the information: yes/no
   - How long settlement will last (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

14. **Whether the settlement is court-enforced or not (if applicable)**
   - Whether the settlement is court-enforced or not (if applicable) - 1: Whether it contains the information: yes/no
   - Whether the settlement is court-enforced or not (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

15. **Appeal (if applicable)**
   - Appeal (if applicable) - 1: Whether it contains the information: yes/no
   - Appeal (if applicable) - 2: Whether the detail information (by which parties and to what court) is correct: (same with the reference) yes/no

16. **Court rulings on any of the important filings (if applicable)**
   This category corresponds with the "important filings" category--so whenever an important filing is mentioned, people also want to know what the ruling on that filing was (if there is one)--e.g., whether the judge granted or denied a motion to dismiss. Generally these filings would be:
   Motions to dismiss
   Motions for summary judgment
   Motions for a preliminary injunction or temporary restraining order
   Motions for class certification
   Motions for attorneys' fees
   Amended complaints--these won't have rulings, so they should be in the "important filings" category but not the "rulings on to important filings" category
   Statements of interest--similar to above, there won't be rulings on these
   - Court rulings on any of the important filings (if applicable) - 1: Whether it contains the information: yes/no
   - Court rulings on any of the important filings (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

17. **Factual basis of case**
   Refers to the facts or evidence upon which the case is built. These facts are essential in the legal process and are used to support legal claims or decisions. It typically includes:
   1. Details of the relevant events – For example, what happened, when it happened, where it happened, and who was involved.  
   2. Evidence – Physical evidence, documentary records, witness testimonies, etc., that support these facts.  
   3. Background information – Context or explanatory facts that provide additional understanding.  
   In legal proceedings, the factual basis is crucial for determining the outcome of a case, as the judge or jury makes decisions based on the facts and the applicable legal principles.
   - Factual basis of case - 1: Whether it contains the information: yes/no
   - Factual basis of case - 2: Whether the detail information is correct: (same with the reference) yes/no

18. **Disputes over settlement enforcement (if applicable)**
   - Disputes over settlement enforcement (if applicable) - 1: Whether it contains the information: yes/no
   - Disputes over settlement enforcement (if applicable) - 2: Whether the detail information is correct: (same with the reference) yes/no

### Output Format
```plaintext
| Checklist Item                                                      | Answer in Ground Truth Summary | Answer in Model Summary | Aggregate |  
|---------------------------------------------------------------------|--------------------------------|-------------------------|-----------|
| Filing Date - 1                                                     |                                |                         |           |
| Filing Date - 2                                                     |                                |                         |           |
| Plaintiff Type - 1                                                  |                                |                         |           |
| Plaintiff Type - 2                                                  |                                |                         |           |
| Cause of Action - 1                                                 |                                |                         |           |
| Cause of Action - 2                                                 |                                |                         |           |
| Statutory Basis for Case - 1                                        |                                |                         |           |
| Statutory Basis for Case - 2                                        |                                |                         |           |
| Statutory Basis for Case - 3                                        |                                |                         |           |
| Remedy Sought - 1                                                   |                                |                         |           |
| Remedy Sought - 2                                                   |                                |                         |           |
| Who are the parties - 1                                             |                                |                         |           |
| Who are the parties - 2                                             |                                |                         |           |
| Note important filings (if applicable) - 1                          |                                |                         |           |
| Note important filings (if applicable) - 2                          |                                |                         |           |
| Significant Terms of decrees (if applicable) - 1                    |                                |                         |           |
| Significant Terms of decrees (if applicable) - 2                    |                                |                         |           |
| Dates of all decrees (if applicable) - 1                            |                                |                         |           |
| Dates of all decrees (if applicable) - 2                            |                                |                         |           |
| How long decrees will last (if applicable) - 1                      |                                |                         |           |
| How long decrees will last (if applicable) - 2                      |                                |                         |           |
| Significant Terms of settlement (if applicable) - 1                 |                                |                         |           |
| Significant Terms of settlement (if applicable) - 2                 |                                |                         |           |
| Date of settlement (if applicable) - 1                              |                                |                         |           |
| Date of settlement (if applicable) - 2                              |                                |                         |           |
| How long settlement will last (if applicable) - 1                   |                                |                         |           |
| How long settlement will last (if applicable) - 2                   |                                |                         |           |
| Whether the settlement is court-enforced or not (if applicable) - 1 |                                |                         |           |
| Whether the settlement is court-enforced or not (if applicable) - 2 |                                |                         |           |
| Appeal (if applicable) - 1                                          |                                |                         |           |
| Appeal (if applicable) - 2                                          |                                |                         |           |
| Court rulings on any of the important filings (if applicable) - 1   |                                |                         |           |
| Court rulings on any of the important filings (if applicable) - 2   |                                |                         |           |
| Factual basis of case - 1                                           |                                |                         |           |
| Factual basis of case - 2                                           |                                |                         |           |
| Disputes over settlement enforcement (if applicable) - 1            |                                |                         |           |
| Disputes over settlement enforcement (if applicable) - 2            |                                |                         |           |
```

Final Score: X%
"""

USE_CASES = [5562, 15895, 589]
PROMPT_DATA_PTH_LLAMA = "data/llama_70b/test_summarized_results.xlsx"
PROMPT_DATA_PTH_GPT = "data/gpt-40/gpt_test_results.xlsx"
PROMPT_DATA_PTH_LEGAL = "data/legal-led-16384/legal-led-16384-test-summarized-results.xlsx"