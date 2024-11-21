import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

from meta import DATASET_PTH, DATASET_OUT_PTH, CASE_ID_COL, COMPLAINT_CNT_COL, APPEAL_CNT_COL, DOCKET_CNT_COL, RESULT_CASE_TYPES_COL

def crawl_info(case_id):
    complaint_count = 0
    appeal_count = 0
    docket_count = 0

    url = f'https://clearinghouse.net/case/{case_id}/'
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # # complaint_count
            # tbody = soup.find('tbody')  # This finds the first <tbody> tag in the HTML  
            # rows = tbody.find_all('tr')  # Find all rows in the <tbody>
            
            # for row in rows:
            #     cells = row.find_all('td')  # Find all cells in the row
            #     if "complaint" in cells[-1].get_text().lower():
            #         complaint_count += 1

            document_collapse_div = soup.find('div', id='documentCollapse')
            if document_collapse_div:
                # Find all 'a' tags with class 'page-link ps-0' inside this div to get the total pages
                total_pages = document_collapse_div.find_all('a', class_='page-link ps-0')
                # print(len(total_pages))
                # print(total_pages)
                if total_pages:
                    text = total_pages[-1].get_text(strip=True)
                    total_pages_num = re.search(r'\d+', text)
                    if total_pages_num:
                        total_pages_num = int(total_pages_num.group())
                else:
                    total_pages_num = 1

                # Initialize complaint_count
                complaint_count = 0

                # Iterate through all pages to count complaints
                for p in range(1, total_pages_num + 1):
                    url = f"https://clearinghouse.net/case/{case_id}/?doc_page={p}#document-list"
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        document_collapse_div = soup.find('div', id='documentCollapse')
                        if document_collapse_div:
                            # Find the table within the div
                            docket_table = document_collapse_div.find('table', class_='table table-striped')
                            if docket_table:
                                tbody = docket_table.find('tbody')
                                if tbody:
                                    # Find all rows in the <tbody>
                                    rows = tbody.find_all('tr')
                                    for row in rows:
                                        cells = row.find_all('td')  # Find all cells in the row
                                        if cells and "complaint" in cells[-1].get_text(strip=True).lower():
                                            complaint_count += 1
                    else:
                        complaint_count = None
                        break  # If a request fails, stop further processing
            else:
                print("Div with id 'documentCollapse' not found.")
                complaint_count = 0

            # appeal_count
            appeal_select = soup.find('select', {'class': 'form-select', 'name': 'select_docket'})
            options = appeal_select.find_all('option')
            appeal_count = len(options)

            # get the case types
            case_types_start = False
            result_case_types = []

            for element in soup.find_all():
                # "Case Types:" <p> find
                if element.name == "p" and element.get_text(strip=True) == "Case Type(s):":
                    case_types_start = True
                    continue  # get texts from the next loop
                
                # stop when find the next <div>
                if case_types_start:
                    if element.name == "div":
                        break
                    if element.name == "p" and "pt-0" in element.get("class", []):
                        result_case_types.append(element.get_text(strip=True))
            
            result_case_type_txt = "\n".join(result_case_types)

            # docket_count
            # get total pages of docket table
            # total_pages = soup.find_all('a', class_='page-link ps-0')
            # print(len(total_pages))
            # print(total_pages)
            # if total_pages:
            #     text = total_pages[-1].get_text(strip=True)
            #     total_pages_num = re.search(r'\d+', text)
            #     if total_pages_num:
            #         total_pages_num = int(total_pages_num.group())
            # else:
            #     total_pages_num = 1

            # # get the number of rows in each page
            # for p in range(1, total_pages_num+1):
            #     url = f"https://clearinghouse.net/case/{case_id}/?docket_page={p}#docket"
            #     response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            #     if response.status_code == 200:
            #         soup = BeautifulSoup(response.content, 'html.parser')
            #         docket_table = soup.find_all('table', class_='table table-striped')
            #         docket_table = docket_table[-1]
            #         if docket_table:
            #             tbody = docket_table.find('tbody')
            #             if tbody:
            #                 docket_rows = tbody.find_all('tr')
            #                 docket_count += len(docket_rows)
            #     else:
            #         docket_count = None

            docket_collapse_div = soup.find('div', id='docketCollapse')
            if docket_collapse_div:
                # Find all 'a' tags with class 'page-link ps-0' inside this div
                total_pages = docket_collapse_div.find_all('a', class_='page-link ps-0')
                # print(len(total_pages))
                # print(total_pages)
                if total_pages:
                    assert len(total_pages) == 1
                    text = total_pages[-1].get_text(strip=True)
                    total_pages_num = re.search(r'\d+', text)
                    if total_pages_num:
                        total_pages_num = int(total_pages_num.group())
                else:
                    total_pages_num = 1

                # Get the number of rows in each page
                docket_count = 0
                for p in range(1, total_pages_num + 1):
                    url = f"https://clearinghouse.net/case/{case_id}/?docket_page={p}#docket"
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        docket_collapse_div = soup.find('div', id='docketCollapse')
                        if docket_collapse_div:
                            docket_table = docket_collapse_div.find('table', class_='table table-striped')
                            if docket_table:
                                tbody = docket_table.find('tbody')
                                if tbody:
                                    docket_rows = tbody.find_all('tr')
                                    docket_count += len(docket_rows)
                    else:
                        docket_count = None
            else:
                print("Div with id 'docketCollapse' not found.")
                docket_count = 0
            
            return complaint_count, appeal_count, docket_count, result_case_type_txt
        else:
            return None, None, None, None
    except Exception as e:
        print(f"Error for case {case_id}: {e}")
        return None, None, None, None

if __name__ == '__main__':
    data = pd.read_excel(DATASET_PTH)
    case_ids = data.iloc[:, 0].unique()
    case_ids = [int(case_id) for case_id in case_ids]

    complaint_counts = []
    appeal_counts = []
    docket_counts = []
    result_case_type_txts = []

    # If an http error occurs, you can start from the case_id where the error occurred.
    # Even though only one case has the error, the error seems to propagate to the following pages, so manual intervention is required.
    case_from = 0
    case_to = 1398
    for case_id in tqdm(case_ids[case_from:case_to]):
        complaint_count, appeal_count, docket_count, result_case_type_txt = crawl_info(case_id)
        complaint_counts.append(complaint_count)
        appeal_counts.append(appeal_count)
        docket_counts.append(docket_count)
        result_case_type_txts.append(result_case_type_txt)
        #print(f"Case ID: {case_id}, Complaint Count: {complaint_count}, Appeal Count: {appeal_count}, Docket Count: {docket_count}")

    out_data = pd.DataFrame({CASE_ID_COL: case_ids[case_from:case_to], COMPLAINT_CNT_COL: complaint_counts, APPEAL_CNT_COL: appeal_counts, DOCKET_CNT_COL: docket_counts, RESULT_CASE_TYPES_COL: result_case_type_txts})

    out_data.to_excel(DATASET_OUT_PTH[:-5]+ f"-{case_from}-{case_to}" + ".xlsx", index=False)