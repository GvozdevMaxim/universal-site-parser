import fake_useragent

SITE_ID = 1

user = fake_useragent.UserAgent().random
header = {'user-Agent': user}
