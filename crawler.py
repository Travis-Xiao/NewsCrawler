import urllib2, re, hashlib, json
from xml.dom import minidom
from datetime import datetime
import beautifier, logger
from multiprocessing import Pool


m = hashlib.md5()
# url domain matcher
p = re.compile(r"://[a-zA-Z0-9.]+\.[a-z]{2,4}")
# error log
l = logger.Logger()
# init time
start_time = datetime.now()
count = 0
category_count = 0
# local hosted server of full feed conversion
service_url = ('http://localhost/fivefilters/makefulltextfeed.php?'
        'max=0&links=preserve&exc=&format=json&submit=Create+Feed'
    )


def crawl(line):
    result = {}
    items = []

    t1 = datetime.now()
    # get domain name of the feed source
    domain = p.search(line)
    # generate identical filename for each source
    file_dir = "./output/"
    if domain:
        file_dir += domain.group()[3:].replace('.', '_')
    else:
        m.update(line)
        file_dir += m.hexdigest()
    output_file = open(file_dir + ".json", "w+")

    item_count = 0

    try:
        # request data from local server
        response = urllib2.urlopen(service_url + '&url=' + line)
        single_page_full_rss = response.read()
        output_file.write(single_page_full_rss)
        output_file.close()

        # get main body of the result and leave the rest behind
        json_rss = json.loads(single_page_full_rss)
        content = json_rss['rss']['channel']['item']
        if type(content) is list:
            # extract restricted info fields from results of five-filters
            for item in content:
                if item['result'] == 'success':
                    newitem = {}
                    newitem['title'] = item['title']
                    newitem['datetime'] = item['pubDate']
                    newitem['content'] = beautifier.beautify(item['description'])
                    newitem['link'] = item['link']
                    items.append(newitem)
                    item_count += 1
                else:
                    l.log("Url extraction failure: \t\t" + item['link'])
        else:
            # extraction failure
            l.log("Feed extraction failure: \t\t" + line)
    except Exception, e:
        print e.message
        pass

    print line

    t2 = datetime.now()
    delta = t2 - t1
    print "Item count: " + str(item_count) + " (" + (str(round(delta.total_seconds() / item_count, 2)) if item_count is not 0 else "0") + "s per item)"
    print "Time elapsed: " + str(delta.total_seconds()) + "s"
    delta = t2 - start_time
    print "Total: " + str(delta.total_seconds()) + "s\n"

    result['count'] = item_count
    result['items'] = items
    return result


def para_crawl(processes=10, rss_xml='rss.opml', result_file='data.json'):
    rss_json = minidom.parse(rss_xml)
    feeds_list = rss_json.getElementsByTagName('outline')
    data_file = open(result_file, "w+")
    pool = Pool(processes=processes)

    # proceed conversion feed by feed
    feeds = []
    for feed in feeds_list:
        line = feed.getAttribute('xmlUrl')
        if len(line) == 0:
            continue
        feeds.append(line)

    _result = pool.map(crawl, feeds)
    _final = []
    _count = 0
    for r in _result:
        _final += r['items']
        _count += r['count']
    json.dump({
        'count': _count,
        'items': _final
    }, data_file)

    print "Complete!"
