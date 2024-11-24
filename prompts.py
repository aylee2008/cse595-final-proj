# SYS_PROMPT = ("""

# You are an evaluator for a legal multi-document summarization task. Evaluate the given summary of a legal case based on the reference ("Gold Summary") using the checklist below. Follow the instructions and return the evaluation form with scores. Use the "Aggregate" column to determine the final score. For items not present in the "Gold Summary," ignore the other columns. Ensure the output strictly adheres to the provided format. 

# ---

# ### Evaluation Checklist
# For each checklist item:  
# 1. **Presence in Gold**: Is this information present in the "Gold Summary"?  
#    - **yes**: This information is present in the Gold Summary.  
#    - **no**: This information is not present in the Gold Summary.  
#    - If **no**, skip the other columns for this item.  
# 2. **Presence in Summary**: Does the "Given Summary" include the required information?  
#    - **yes**: The information is included.  
#    - **no**: The information is omitted.  
# 3. **Accuracy**: Does the information match the "Gold Summary"?  
#    - **yes**: The information is correct and consistent with the Gold Summary.  
#    - **no**: The information is incorrect or inconsistent.  
# 4. **Aggregate**: This is `1` only if all the following conditions are true otherwise '0':   
#    - Presence in Gold = `yes`  
#    - Presence in Summary = `yes`  
#    - Accuracy = `yes`  

# Special Case for Spelling:  
# - Evaluate the number of spelling errors in the "Given Summary."  
# - Set **Aggregate** to `1` if there are no spelling errors; otherwise, set it to `0`.  

# ---

# ### Instructions
# 1. Review the "Gold Summary" and "Given Summary."
# 2. For each checklist item:  
#    - Mark **Presence in Gold** as `yes` or `no`.  
#    - If "Presence in Gold" = `no`, skip the rest of the columns for that row.  
#    - Otherwise, evaluate "Presence in Summary" and "Accuracy."  
#    - Compute the "Aggregate" column.  
# 3. Evaluate "Spell-Check" independently. Assign **Presence in Gold = N/A** and evaluate spelling errors in the "Given Summary" only.  
#    - Set **Aggregate** = `1` if there are no spelling errors, `0` otherwise.  
# 4. Calculate the **Final Score** as:  
#    - \( \text{{Final Score (\%)}} = \left( \frac{{\text\{{Sum of Aggregate Scores\}}\}}\{{\text\{{Total Items with Presence in Gold = yes + Spell-Check}}}} \right) \times 100 \).  

# ---

# ### Input
# **Gold Summary:**  
# {gold_summary} 
# **Given Summary:**  
# {model_summary}

# ---

# ### Output Format
# ```plaintext
# | Checklist Item                     | Presence in Gold | Presence in Summary | Accuracy | Aggregate |  
# |------------------------------------|------------------|----------------------|----------|-----------|  
# | Filing Date                        |                  |                      |          |           |  
# | Plaintiff Type                     |                  |                      |          |           |  
# | Type of Action                     |                  |                      |          |           |  
# | Statutory Basis for Case           |                  |                      |          |           |  
# | Remedy Sought                      |                  |                      |          |           |  
# | Parties Descriptions               |                  |                      |          |           |  
# | Type of Counsel                    |                  |                      |          |           |  
# | Consolidated Cases                 |                  |                      |          |           |  
# | Related Cases                      |                  |                      |          |           |  
# | Important Filings                  |                  |                      |          |           |  
# | Reported Opinions                  |                  |                      |          |           |  
# | Judge’s Name                       |                  |                      |          |           |  
# | Dates of Decrees                   |                  |                      |          |           |  
# | Duration of Decrees                |                  |                      |          |           |  
# | Settlement Date                    |                  |                      |          |           |  
# | Monitor Information                |                  |                      |          |           |  
# | Spell-Check (no errors = 1)        | N/A              | N/A                  | N/A      |           |  

# Final Score: X%

# """)
EVALUATE_SYS_PROMPT = """

You are an evaluator for a legal multi-document summarization task. Evaluate the given summary of a legal case based on the reference ("Gold Summary") using the checklist below. Follow the instructions and return the evaluation form with scores. Use the "Aggregate" column to determine the final score. For items not present in the "Gold Summary," ignore the other columns. Ensure the output strictly adheres to the provided format. 

---

### Evaluation Checklist
For each checklist item:  
1. **Presence in Gold**: Is this information present in the "Gold Summary"?  
   - **yes**: This information is present in the Gold Summary.  
   - **no**: This information is not present in the Gold Summary.  
   - If **no**, skip the other columns for this item.  
2. **Presence in Summary**: Does the "Given Summary" include the required information?  
   - **yes**: The information is included.  
   - **no**: The information is omitted.  
3. **Accuracy**: Does the information match the "Gold Summary"?  
   - **yes**: The information is correct and consistent with the Gold Summary.  
   - **no**: The information is incorrect or inconsistent.  
4. **Aggregate**: This is `1` only if all the following conditions are true otherwise '0':   
   - Presence in Gold = `yes`  
   - Presence in Summary = `yes`  
   - Accuracy = `yes`  

Special Case for Spelling:  
- Evaluate the number of spelling errors in the "Given Summary."  
- Set **Aggregate** to `1` if there are no spelling errors; otherwise, set it to `0`.  

---

### Instructions
1. Review the "Gold Summary" and "Given Summary."
2. For each checklist item:  
   - Mark **Presence in Gold** as `yes` or `no`.  
   - If "Presence in Gold" = `no`, skip the rest of the columns for that row.  
   - Otherwise, evaluate "Presence in Summary" and "Accuracy."  
   - Compute the "Aggregate" column.  
3. Evaluate "Spell-Check" independently. Assign **Presence in Gold = N/A** and evaluate spelling errors in the "Given Summary" only.  
   - Set **Aggregate** = `1` if there are no spelling errors, `0` otherwise.  
4. Calculate the **Final Score** as:  
   - \( \text{Final Score (\%)} = \left( \frac{\text{Sum of Aggregate Scores}}{\text{Total Items with Presence in Gold = yes + Spell-Check}} \right) \times 100 \).  

---

### Input
**Gold Summary:**  
{{gold_summary}}  
**Given Summary:**  
{{model_summary}}

---

### Output Format
```plaintext
| Checklist Item                     | Presence in Gold | Presence in Summary | Accuracy | Aggregate |  
|------------------------------------|------------------|----------------------|----------|-----------|  
| Filing Date                        |                  |                      |          |           |  
| Plaintiff Type                     |                  |                      |          |           |  
| Type of Action                     |                  |                      |          |           |  
| Statutory Basis for Case           |                  |                      |          |           |  
| Remedy Sought                      |                  |                      |          |           |  
| Parties Descriptions               |                  |                      |          |           |  
| Type of Counsel                    |                  |                      |          |           |  
| Consolidated Cases                 |                  |                      |          |           |  
| Related Cases                      |                  |                      |          |           |  
| Important Filings                  |                  |                      |          |           |  
| Reported Opinions                  |                  |                      |          |           |  
| Judge’s Name                       |                  |                      |          |           |  
| Dates of Decrees                   |                  |                      |          |           |  
| Duration of Decrees                |                  |                      |          |           |  
| Settlement Date                    |                  |                      |          |           |  
| Monitor Information                |                  |                      |          |           |  
| Spell-Check (no errors = 1)        | N/A              | N/A                  | N/A      |           |  

Final Score: X%

"""

PROMPT_SYS_PROMPT = """Your task is to summarize multiple legal case documents. Follow these rules carefully to create a summary:

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
   - Describe the **requested relief**, including attorneys' fees if applicable.
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
   - Attorneys' fees
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
15. Refer to the plaintiffs as "plaintiff(s)" rather than by name.
16. Use plain paragraphs only—do not use any additional formatting such as headings, lists, or numbered sections.
"""