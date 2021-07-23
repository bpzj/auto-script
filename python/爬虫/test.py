import re

pattern = re.compile(r'.{4}年[一二]{0,2}月?')
print(pattern.findall('同苏修大使契尔沃年科的谈话（一九六三年）.tex'))
print(pattern.findall('同苏修大使契尔沃年科的谈话（一九六三年二月二十三日）.tex'))

