import re
import requests
from bs4 import BeautifulSoup



def parse_stats(stats):
    total_cases = 0
    total_deaths = 0

    for line in stats:
        line = str(line)
        if ("Total cases" in line) or ("confirmed cases" in line):
            total_cases = int(re.findall(r'\b\d+\b', line)[0])
        elif "deaths" in line:
            total_deaths = int(re.findall(r'\b\d+\b', line)[0])

    return (total_cases, total_deaths)


def get_us_stats():
    """
    Uses BeautifulSoup to get current national COVID-19 stats from CDC.
    Returns a tuple in the format (total cases, total deaths).
    """
    response = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html")

    soup = BeautifulSoup(response.content, "html.parser")
    summary_div = soup.find("div", {"class": "2019coronavirus-summary"})
    stats = summary_div.find_all("li")

    return parse_stats(stats)


def get_kingcounty_stats():
    response = requests.get("https://www.kingcounty.gov/depts/health/communicable-diseases/disease-control/novel-coronavirus.aspx")

    soup = BeautifulSoup(response.content, "html.parser")
    summary_div = soup.find_all("div", {"class": "col-sm-8"})
    summary_div = summary_div[1].find("div", {"class": "panel-body"})
    stats = summary_div.find_all("li")

    return(parse_stats(stats))
    