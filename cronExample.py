from crontab import CronTab

# cron = CronTab(user=True,tabfile="""* * * * * command""")  
# job = cron.new(command='python example1.py')  
# job.minute.every(1)

# cron.write() 
# file_cron = CronTab(tabfile='filename.tab')
# cron = CronTab(tab="""
#   * * * * * python D:/Cardo/uc/sem 2/MYOB/code/example1.py
# """)
my_cron = CronTab(user='cardr')
for job in my_cron:
	print(job)
# job = cron.new()  
# job.minute.every(1)
# cron.write()
# job  = cron.new(command='pwd')