import time
import os
from selenium.webdriver import Chrome, ChromeOptions, DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException


class GoogleSpider:
    driver = None
    keyword = None
    time_out = 1

    def __init__(self,
                 keyword,
                 proxy_server,
                 thread_count=5,
                 chrome_dir='ChromeData',
                 chrome_path='chrome',
                 chrome_port=9787,
                 ):
        self.keyword = keyword
        # selenium远程连接Chrome
        # 代理 例--proxy-server=socks5://127.0.0.1:9090
        os.popen(
            '{} --remote-debugging-port={} --user-data-dir={} {}'.format(chrome_path, chrome_port, chrome_dir, '--proxy-server=' + proxy_server if proxy_server else ''))
        options = ChromeOptions()

        # 远程连接Chrome
        options.add_experimental_option(
            'debuggerAddress', '127.0.0.1:{}'.format(chrome_port))

        desired_capabilities = DesiredCapabilities().CHROME
        desired_capabilities['pageLoadStrategy'] = 'none'
        self.driver = Chrome(
            options=options, desired_capabilities=desired_capabilities)
        super().__init__()

    def driver_get(self, url):
        self.driver.get(url)
        time.sleep(self.time_out)
        while 'www.google.com/sorry' in self.driver.current_url:
            time.sleep(1)

    def start(self):
        def parse_article_url():
            while 'www.google.com/sorry' in self.driver.current_url:
                time.sleep(1)
            time.sleep(2)
            for i in self.driver.find_elements_by_class_name('g'):
                url = i.find_element_by_tag_name(
                    'a').get_attribute('href').strip()
                if 'https://www.google.com/' not in url:
                    print(url)

                    with open('google.txt', 'a') as f:
                        f.write(url + '\n')

        self.driver_get(
            'https://www.google.com/search?q={}'.format(self.keyword))
        time.sleep(2)
        while True:
            while True:
                try:
                    parse_article_url()
                    break
                except NoSuchElementException as e:
                    print(e)
                    time.sleep(1)
            try:
                while 'www.google.com/sorry' in self.driver.current_url:
                    time.sleep(1)
                next_element = self.driver.find_element_by_id('pnnext')
                if not next_element:
                    next_element = self.driver.find_element_by_partial_link_text(
                        'Next')

                if not next_element:
                    next_element = self.driver.find_element_by_partial_link_text(
                        '下一页')
                if not next_element:
                    next_element = self.driver.find_element_by_partial_link_text(
                        '下一頁')
                next_element.click()
            except NoSuchElementException as __:
                self.time_out += 1
                if self.time_out >= 10:
                    break
