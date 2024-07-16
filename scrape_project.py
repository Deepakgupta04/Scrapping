import requests
from bs4 import BeautifulSoup
import json

# URL of the site
url = 'https://hprera.nic.in/PublicDashboard'

# Send a GET request to the URL
response = requests.get(url)

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the registered projects
projects_table = soup.find('table', {'id': 'projectDetails'})

# Extract the first 6 project rows (excluding the header row)
projects = projects_table.find_all('tr')[1:7]

# List to store project details
project_details = []

# Function to get project detail from detail page
def get_project_detail(detail_url):
    response = requests.get(detail_url)
    detail_soup = BeautifulSoup(response.content, 'html.parser')
    details = {}

    # Extract GSTIN No, PAN No, Name, and Permanent Address from the detail page
    details['GSTIN No'] = detail_soup.find('span', {'id': 'GSTIN'}).text.strip()
    details['PAN No'] = detail_soup.find('span', {'id': 'PAN'}).text.strip()
    details['Name'] = detail_soup.find('span', {'id': 'PromoterName'}).text.strip()
    details['Permanent Address'] = detail_soup.find('span', {'id': 'PromoterAddress'}).text.strip()
    
    return details

# Iterate over the first 6 projects and get their details
for project in projects:
    cells = project.find_all('td')
    if len(cells) > 0:
        project_link = cells[1].find('a')['href']
        detail_url = 'https://hprera.nic.in' + project_link
        
        # Get project detail
        detail = get_project_detail(detail_url)
        project_details.append(detail)

# Print the project details
for idx, detail in enumerate(project_details, start=1):
    print(f"Project {idx}:")
    for key, value in detail.items():
        print(f"{key}: {value}")
    print()

# Saving to a file for the result
with open('project_details.json', 'w') as f:
    json.dump(project_details, f, indent=4)
