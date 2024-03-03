import datetime 

numdays = 364
base = datetime.datetime.now()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_list2 = [f'{t.year}-{t.month}-{t.day}' for t in date_list]
print(date_list2)
