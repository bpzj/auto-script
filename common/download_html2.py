import requests


def download_file(url: str, file_name: str):
    r = requests.get(url)
    # 获取当前编码 当前编码有utf-8 ISO-8859-1
    # 新建一个文件名 例如：TencentHtml 设置文件格式编码为 utf-8
    # 注意文件格式的编码和 获取的编码 要一致，不然出现乱码问题
    with open(file_name, 'w') as file:
        file.write(r.text)


if __name__ == '__main__':
    # download_file('https://docs.spring.io/spring-framework/docs/5.0.x/spring-framework-reference/core.html', 'core.html')
    # download_file('http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css', 'stylesheets/font-awesome.min.css')
    # download_file('https://docs.spring.io/spring-framework/docs/5.0.x/spring-framework-reference/stylesheets/asciidoctor-spring.css', 'stylesheets/asciidoctor-spring.css')
    download_file('https://docs.spring.io/spring-framework/docs/5.0.x/spring-framework-reference/tocbot-3.0.2/tocbot.css', 'tocbot-3.0.2/tocbot.css')
