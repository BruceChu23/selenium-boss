from jobspider import Job

j = input('输入你要获取的职业关键词：')
url = input('输入你要爬取的Boss直聘中的网址：')
pages = input('输入你要获取的页数：')
job = Job(j, url, pages)
job.give_me_job()
