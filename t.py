# 本页是知识补充：练习定位元素的不同写法。

from bs4 import BeautifulSoup

html = """
<table id="courses" class="data-table">
  <tr class="header">
    <th>课程</th><th>教师</th><th>地点</th>
  </tr>
  <tr class="course-row">
    <td class="name">Python程序设计</td>
    <td class="teacher">张老师</td>
    <td class="room">A101</td>
  </tr>
  <tr class="course-row">
    <td class="name">大学英语</td>
    <td class="teacher">李老师</td>
    <td class="room">B203</td>
  </tr>
</table>
"""

soup = BeautifulSoup(html, "html.parser")

table1 = soup.find("table")                         # 按标签名找
table2 = soup.find("table", id="courses")           # 按属性找
table3 = soup.select_one("#courses")                # CSS 选择器：# 表示 id

print(table1 is table2 is table3)

rows = soup.select("#courses tr.course-row")        # 只找课程数据行
for row in rows:
    name = row.select_one(".name").get_text(strip=True)
    teacher = row.select_one(".teacher").get_text(strip=True)
    room = row.select_one(".room").get_text(strip=True)
    print(name, teacher, room)