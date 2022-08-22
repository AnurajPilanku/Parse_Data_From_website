import csv
import requests
from bs4 import BeautifulSoup

# Group | Category | code | long desc | short desc | 
def scrape_data(base_url):
    codes_url = base_url + "/Codes"
    response = requests.get(codes_url, timeout=1000)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.select('tbody > tr')
    data = []

    # group | Category
    for row in rows:
        row_data = {}
        columns = row.find_all('td')
        row_data["group"] = columns[0].text
        row_data["category"] = columns[2].text
        group_link = columns[0].find('a')['href']
        group_url = base_url + group_link
        row_data["group_url"] = group_url
        data.append(row_data)

    second_phase = []
    for row_data in data:
        response = requests.get(row_data["group_url"], timeout=1000)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table')[0]
        rows = table.select('tbody > tr')
        for row in rows:
            row_data_second_phase = {}
            row_data_second_phase["group"] = row_data["group"]
            row_data_second_phase["category"] = row_data["category"]
            columns = row.find_all('td')
            row_data_second_phase["code"] = columns[0].text
            row_data_second_phase["long_desc"] = columns[1].text
            short_desc_link = columns[0].find('a')['href']
            short_desc_url = base_url + short_desc_link
            row_data_second_phase["short_desc_url"] = short_desc_url
            second_phase.append(row_data_second_phase)

    third_phase = []

    for row_datum in second_phase:
        response = requests.get(row_datum["short_desc_url"], timeout=1000)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')
        if tables:
            table = tables[0]
            rows = table.select('tbody > tr')
            for row in rows:
                row_data_third_phase = {}
                row_data_third_phase["Group"] = row_datum["group"]
                row_data_third_phase["Category"] = row_datum["category"]
                columns = row.find_all('td')
                row_data_third_phase["Code"] = row_datum["code"]
                row_data_third_phase["Long Description"] = row_datum["long_desc"]
                columns = row.find_all("td")
                row_data_third_phase["Short Description"] = columns[0].text
                third_phase.append(row_data_third_phase)
    return third_phase

def write_to_csv(collected_data):
    field_names = ['Group', 'Category', 'Code', 'Long Description', 'Short Description']
    with open('output.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(collected_data)

def main():
    import pdb;pdb.set_trace()
    base_url = "https://www.hcpcsdata.com"
    collected_data = scrape_data(base_url)
    write_to_csv(collected_data)

main()