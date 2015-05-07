import multiprocessing
import crawler


if __name__ == '__main__':
    multiprocessing.freeze_support()
    crawler.para_crawl(10)


