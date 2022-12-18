import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title =[]
company_name =[]
location_name =[]
job_skill =[]
date =[]
page_num =0

while True:
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=spbg&q=digital%20marketing&start={page_num}")
        src = result.content
        soup = BeautifulSoup(src,"lxml")

        page_limit = float(soup.find("strong").text)
        if(page_num > page_limit / 15):
            print("pages ended ,terminate")
            break

        job_titles = soup.find_all("h2",{"class":"css-m604qf"})
        company_names = soup.find_all("a",{"class":"css-17s97q8"})
        locations_names = soup.find_all("span" , {"class":"css-5wys0k"})
        job_skills = soup.find_all("div",{"class":"css-y4udm8"})
        posted_new = soup.find_all("div",{"class":"css-4c4ojb"})
        posted_old = soup.find_all("div",{"class":"css-do6t5g"})
        posted =[*posted_old ,*posted_new]

        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            company_name.append(company_names[i].text)
            location_name.append(locations_names[i].text)
            job_skill.append(job_skills[i].text)
            date.append(posted[i].text)
        page_num += 1
        print("page switched")
    except:
        print("error")
        break

file_list =[job_title,company_name,date,location_name,job_skill]
exported=zip_longest(*file_list)
with open("/pythonProject/jobstest.csv","w") as myfile :
    wr = csv.writer(myfile)
    wr.writerow(["job title", "company name","date" ,"location", "skills"])
    wr.writerows(exported)
