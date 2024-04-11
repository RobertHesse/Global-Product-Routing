Run userRouting.py as the main app. 
We could make cron job for these tasks:
1. getting all sitemaps once a week
2. get all products once per day
3. create linking table once per day
4. keep userRouting.py running as routing service

Requirements
1. We need a seperate domain (would propose stauff.digital as the domain) 
2. We need a server to run python on (own linux server)

What are disadvantaged? 
1. Products have to be listed on the sitemap.xml
2. alternatevly we could create a sitemap.html which is independent from search engine visibility
