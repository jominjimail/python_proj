import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
print(page)

print(page.status_code)
print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

print(list(soup.children))

print([type(item) for item in list(soup.children)])
print("\n")
html = list(soup.children)[2]
print (html)
print("\n")
body = list(html.children)[3]
print(body)
print("\n")
p=list(body.children)[1]
print(p)
print("\n")
soup.find_all('p')
print(soup.find_all('p'))

soup.find_all('p')[0].get_text()
