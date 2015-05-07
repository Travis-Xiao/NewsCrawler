import re

preserve_carriage_regex = r'</p>'
html_tag_regex = r'<("[^"]*"|\'[^\']*\'|[^\'">])*>'
redundant_blank_regex = r'\s{2,}'
content_regex = r'[^\x00-\x7FA-Za-z0-9:\.!@#\$%\*\(\)\n\'\",\-\+\[\]\{\} ]'


def beautify(s):
    t = re.sub(preserve_carriage_regex, '\n', s.decode('unicode-escape'))
    t = re.sub(html_tag_regex, ' ', t)
    t = re.sub(content_regex, ' ', t)
    return re.sub(redundant_blank_regex, ' ', t)
