import requests

prefix = 'https://www.marxists.org/chinese/maozedong/1968/'


def get_number(param):
    if param:
        mark = '</center>'
        param = param[:param.index(mark)]
        start = param.index('<b>')
        end = param.index('</b>')
        return param[start + 3:end].replace('）', '').replace(' ', '') + '-'
    else:
        return ''


def get_date(content):
    mark = '<p class=\'date\'>'
    if mark in content:
        idx = content.index(mark) + len(mark)
        date = content[idx:content.index('</p>')]
        content = content[content.index('</p>') + 4:]
        return date, content
    else:
        return None, content


def get_date_number(date: str):
    if date:
        if ('日' in date):
            date = date[:date.index('日')]
        elif ('月' in date):
            date = date[:date.index('月')]
        elif ('年' in date):
            date = date[:date.index('年')]
        else:
            return ''
        no = date.replace('（', '').replace('）', '')
        no = no.replace('年', '.').replace('月', '.').replace('日', '')
        no = no.replace('二十', '2').replace('廿', '2').replace('十', '1').replace('○', '0')
        no = no.replace('一', '1').replace('二', '2').replace('三', '3').replace('四', '4').replace('五', '5')
        no = no.replace('六', '6').replace('七', '7').replace('八', '8').replace('九', '9').replace('零', '0')
        return no + '-'
    else:
        return ''


def get_title(html):
    title = html[:html.index('1968年汉版《毛泽东思想万岁》')]
    title = title[title.index('<title>') + 7:title.index('</title>')]
    return title


def store_as_tex(url):
    res = requests.get(prefix + url)
    html = res.content.decode('gbk')
    title = get_title(html)

    left = html[html.index('1968年汉版《毛泽东思想万岁》'):]
    number = get_number(left)

    left = left[left.index('</p>\r\n<br>') + 10:]

    left = left.replace('<br>', '').replace('\u3000', '')

    mark = '<p style="text-align: center; font-size: 11pt; line-height:100%; margin-top:5pt">'
    idx1 = left.index(mark)
    content = left[:idx1]
    left = left[idx1 + len(mark):]
    content = content.replace('\r\n\r\n\r\n\r\n', '\n\n')
    content = content.replace('<hr size=\'1\'>', '')
    content = content.replace('&nbsp;', '')
    content = content.replace('<p><font face="宋体">', '')

    left = left[left.index('目录'):left.index('下一页')]
    next_htm = left[left.index('href="') + 6:left.index('" title=')]
    date, content = get_date(content)
    date_no = get_date_number(date)
    with open(number + date_no + title + '.tex', 'wb') as f:
        f.write(r'\section{'.encode('utf-8') + title.encode('utf-8') + '}\n'.encode('utf-8'))
        if date:
            f.write(r'\datesubtitle{'.encode() + date.encode() + '}\n'.encode())
        f.write(content.encode('utf-8'))
    return next_htm


url = '1-029.htm'
while url:
    print(url + ' start')
    url = store_as_tex(url)
