prompt = """
Task: Evaluate a generated summary against a gold-standard summary using the provided rubric.
Planer Role: Identify which checklist items should be addressed by each expert-role LLM team member.
Expert Roles and Responsibilities:
Case Historian: Verify basic facts and the chronological order of the case.
Legal Analyst: Assess the legal basis and accuracy of cited statutes.
Litigation Context Evaluator: Evaluate the case background and the roles of involved parties.
Remedy and Outcome Reviewer: Review judgments and remedies.
Procedural Specialist: Check case procedures and documentation.
Provide evaluation results on each checklist item. 
Output the accuracy, calculated as the number of "yes" responses divided by the total number of questions.

Gold-standard summary:"
"

Generated summary: "
"

Rubric:
Filing Date
- Whether it contains the Date: yes/no
- Whether the Date is correct (compare with the reference): yes/no
  - yes: the summary contains consistent and correct dates;
  - no: some or all filling date information is incorrect
Class Action or Individual Plaintiffs? (if applicable)
  - Description: If there are class action plaintiffs the summary should say it's a class action; if there are individual plaintiffs it can just describe the plaintiffs. For example, use specific terms like "The city" or "The parents" rather than general terms like "The defendant" or "The plaintiffs."
  - Whether it contains the information: yes/no
    - yes: the summary clearly states the plaintiff information
    - no: do not mention whether it’s a class action or individual plaintiffs
  - Whether the detailed information is correct: if there are class action plaintiffs the summary should say it's a class action; if there are individual plaintiffs the summary can just describe the plaintiffs (same with the reference): yes/no
    - yes: the summary consistently and correctly states whether it is a Class Action or Individual Plaintiffs (describe the plaintiffs).
    - no: the summary does not consistently and correctly state whether it is a Class Action or Individual Plaintiffs (describe the plaintiffs).
Cause of Action
  - Description: eg. a statute (e.g. 42 USC 1983) or a case (e.g. Ex Parte Young)
  - Whether it contains the information: yes/no
    - yes: the summary clearly states the action information
    - no: do not mention the action information
  - Whether the detailed information is correct: (same with the reference): yes/no 
    - yes: the summary consistently and correctly states the type of action
    - no: mention the wrong action information
Statutory or Constitutional Basis for the Case
  - Description: A case can either be based on a statute or a provision of the Constitution--i.e., a case will either claim that someone violated a statute, or violated the Constitution. For cases that have a constitutional basis, the summary should refer to the clause of the Constitution that was allegedly violated, as well as the amendment if applicable. So for example it would say "the plaintiffs alleged violations of the Fourteenth Amendment's Equal Protection Clause," or "the plaintiffs alleged violations of the Commerce Clause."
  - Whether it claim that someone violated a statute or violated the Constitution: yes, no
  - Whether it contains the statutory bases information or constitutional bases information: yes/no
    - yes: contains the statutory bases or constitutional bases information
    - no: do not contain any statutory basis or constitutional bases information
  - Whether the detailed information is correct: what are the statutory bases? (same with the reference): yes/no
    - yes: contains all the right statutory bases
    - no: do not contains all the right statutory bases
Remedy Sought 
  - Description: eg. declaratory judgment
    - Whether it contains the information: yes/no
    - Whether the detail information is correct: (same with the reference): yes/no
Who are the parties (description, not name)?
  - Whether it contains the information: yes/no
    - Whether it contains the plaintiff information
    - Whether it contains the description of the defendants (usually based on their office/position if it's a government official): yes/no
  - Whether the detail information is correct: (same with the reference)
    - Is the plaintiff correct? yes/no
    - Is the defendant correct? yes/no
Note important filings (if applicable)
  - Description: Note important filings including motions for temporary restraining orders or preliminary injunctions, motions to dismiss, motions for summary judgment, etc. 
    - Whether the reference includes this information and the generated result also includes it, or the reference does not include this information and the generated result also does not include it: yes/no
    - Whether the detail information is correct: (same with the reference)
      - Are the types of filings correct? yes/no
Significant Terms of decrees (if applicable)
  - Description
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
  - Whether it contains details about the significant terms: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Dates of all decrees (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
How long decrees will last (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Significant Terms of settlement (if applicable)
  - Whether it contains details about the significant terms: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Date of settlement (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
How long settlement will last (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Whether the settlement is court-enforced or not (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Appeal (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information (by which parties and to what court) is correct: (same with the reference) yes/no
Court rulings on any of the important filings (if applicable)
  - Description: This category corresponds with the "important filings" category--so whenever an important filing is mentioned, people also want to know what the ruling on that filing was (if there is one)--e.g., whether the judge granted or denied a motion to dismiss. Generally these filings would be:
    Motions to dismiss
    Motions for summary judgment
    Motions for a preliminary injunction or temporary restraining order
    Motions for class certification
    Motions for attorneys' fees
    Amended complaints--these won't have rulings, so they should be in the "important filings" category but not the "rulings on to important filings" category
    Statements of interest--similar to above, there won't be rulings on these
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Factual basis of case
  - Description 
    Refers to the facts or evidence upon which the case is built. These facts are essential in the legal process and are used to support legal claims or decisions. It typically includes:
    1. Details of the relevant events – For example, what happened, when it happened, where it happened, and who was involved. 
    2. Evidence – Physical evidence, documentary records, witness testimonies, etc., that support these facts. 
    3. Background information – Context or explanatory facts that provide additional understanding. 
    In legal proceedings, the factual basis is crucial for determining the outcome of a case, as the judge or jury makes decisions based on the facts and the applicable legal principles.
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
Disputes over settlement enforcement (if applicable)
  - Whether it contains the information: yes/no
  - Whether the detail information is correct: (same with the reference) yes/no
"""
