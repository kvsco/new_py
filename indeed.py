import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("ul", {"class": "pagination-list"})

    links = pagination.find_all('a')
    pages = []
    for link in links[0:-1]:
      pages.append(int(link.find("span").string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("h2", {"class": "title"})
    title_anchor = title.find("a")["title"]

    company = html.find("span", {"class": "company"})
    if company:
      company_anchor = company.find("a")
      if company_anchor is not None:
          company = str(company_anchor.string)
      else:
          company = str(company.string)
      company = company.strip()
    else:
      company = None
      
    location = html.find("div", {"class": "recJobLoc"})['data-rc-loc']
    job_id = html.find("h2", {"class": "title"}).find("a")["href"]

    return {
        'title': title_anchor,
        'company': company,
        "location": location,
        "link": f"https://kr.indeed.com{job_id}"
    }


def extract_get_jobs(last_page): 
                              ##last_page = 5
    jobs = []
    for page in range(last_page):
      print(f"Scrapping Indeed page: {page}" )
      result = requests.get(f"{URL}&start={page*LIMIT}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs



def get_jobs():
  last_page = get_last_page()
  ## maxpage = 5 =last_page 
  jobs = extract_get_jobs(last_page)

  return jobs