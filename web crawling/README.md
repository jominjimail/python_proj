## Beautiful Soup Documentation

[Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[실습 내용](https://www.dataquest.io/blog/web-scraping-tutorial-python/)



*html 기본 구조를 할 고 있어야 함*

*python 3.x version 사용*



#### 설치 목록

- pandas
- bs4



#### 기본 사용법 

```python
import requests

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")

print(page) # <Response[200]>
print(page.status_code) # 200
print(page.content) # ... content ...
```

- 실습에 사용할 sample web page에 접근하기 위해 requests.get method 사용
- 200이라는 뜻은 page download가 성공했다는 뜻이다. 

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(page.content, 'html.parser')
```

- Beautifulsoup library를 이용해서 page.content를 parse를 할 것이다.

```python
soup.prettify() # print formatted
'''
<!DOCTYPE html>
<html>
 <head>
  <title>
   A simple example page
  </title>
 </head>
 <body>
  <p>
   Here is some simple content for this page.
  </p>
 </body>
</html>
'''
```

- 파싱이 된 page.content에서 foramt에 대한 정보를 얻을 수 있다.

```python
list(soup.children) # print children
'''
['html', '\n', <html>
 <head>
 <title>A simple example page</title>
 </head>
 <body>
 <p>Here is some simple content for this page.</p>
 </body>
 </html>]
'''
```

- children의 return값은 list이다. 
- 위 결과값으로 2개의 상위 tag정보를 알 수 있다. <!DOCTYPE html>  tag, <html> tag

```python
[type(item) for item in list(soup.children)] #print type
'''
[bs4.element.Doctype, bs4.element.NavigableString, bs4.element.Tag]
'''
```

- 해당 children의 type을 알 수 있다.
- *Doctype*은 document의 타입을 나타낸다.
- *NavigableString*은 HTML document에서 text를 찾았다는 의미이다.
- *Tag*은 다른 모든 tag를 의미하다.
- 우린 *Tag*부분에 주목할 것이다.

```python
html = list(soup.children)[2]
list(html.children) #print children
'''
['\n', <head>
 <title>A simple example page</title>
 </head>, '\n', <body>
 <p>Here is some simple content for this page.</p>
 </body>, '\n']
'''
```

- children의 return 값은 list이다.
- 위 결과값으로 2개의 상위 tag정보를 알 수 있다. <head>  tag, <body> tag
- <body> 안에 있는 <p> 값에 접근해보자.

```python
body = list(html.children)[3]
list(body.children) # print children
'''
['\n', <p>Here is some simple content for this page.</p>, '\n']
'''
```

- [3]은 <body> 부분을 가리킨다.
- <body>의 children을 출력해보면 상위 tag인 <p> 정보를 알 수 있다.

```python
p = list(body.children)[1]
p.get_text() # print text 
'''
'Here is some simple content for this page.'
'''
```

- tag안에 있는 text를 출력하기 위해 get_text() method를 사용한다.





#### 응용 사용법

모든 instance의 tag를 한번에 찾는 방법을 소개할 것이다.

```python
soup = BeautifulSoup(page.content, 'html.parser')
soup.find_all('p') # print finded
'''
[<p>Here is some simple content for this page.</p>]
'''
```

- find_all() method을 사용하면 해당 page의 모든 instance중 <p> 를 찾을 수 있다.
- find_all() 의 return 값은 list이다. 

```python
soup.find_all('p')[0].get_text()
'''
'Here is some simple content for this page.'
'''
```

- 각각의 text 정보를 알고 싶다면 loop를 이용해 출력하면 된다.

```python
soup.find('p')
'''
<p>Here is some simple content for this page.</p>
'''
```

- 모든 <p>을 찾고 싶은게 아니라 first instance의 <p> tag을 알고 싶다면 find() method를 사용하면 된다.



#### class와 id으로 tag 찾기

class 와 id는 CSS에서 사용된다. HTML의 element를 구별하기 위해서 분류된 class나 id를 이용해 style을 지정할 수 있다. 또한 scrape할 때도 사용된다.

해당 실습을 위해 page부분의 url을 수정해준다.

```python
page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser') #print it
'''
<html>
<head>
<title>A simple example page</title>
</head>
<body>
<div>
<p class="inner-text first-item" id="first">
                First paragraph.
            </p>
<p class="inner-text">
                Second paragraph.
            </p>
</div>
<p class="outer-text first-item" id="second">
<b>
                First outer paragraph.
            </b>
</p>
<p class="outer-text">
<b>
                Second outer paragraph.
            </b>
</p>
</body>
</html>
'''
```

```python
soup.find_all('p', class_='outer-text') #print
'''
[<p class="outer-text first-item" id="second">
 <b>
                 First outer paragraph.
             </b>
 </p>, <p class="outer-text">
 <b>
                 Second outer paragraph.
             </b>
 </p>]
'''
```

- class을 사용해 찾기위해 fild_all() method를 사용한다.
- *outer-text* class를 가지고 있는 모든 <p> 가 출력된다.

```python
soup.find_all(class_="outer-text") #print
'''
[<p class="outer-text first-item" id="second">
 <b>
                 First outer paragraph.
             </b>
 </p>, <p class="outer-text">
 <b>
                 Second outer paragraph.
             </b>
 </p>]
'''
```

- 위와 동일한 결과가 나왔다. 
- 하지만, <p> 속성은 아니지만 class이가 *outer-text*인 instance가 있다면 추가 출력이 되었을 것이다.

```python
soup.find_all(id="first") #print
'''
[<p class="inner-text first-item" id="first">
                 First paragraph.
             </p>]
'''
```

- *first* id을 가지고 있는 모든 instance가 출력되었다.



#### CSS 의 selector사용해서 Search하기

