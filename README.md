# FBScraper
FB groups scraper in Python 2.7 <br />
<br />
ABOUT THE PROJECT: <br />
This is one of my first projects using the Python language.<br />
It was created to deepen my knowlage in python and help filter the information needed for me.<br />
Written for the groups that does not support using Graph API.<br />
It scans posts, scrapes them into a Post data structure and saves it to DB.<br />
Then it loads unread posts and shows it on App UI table.<br />
There, it can be marked as to send cv by mail or mark as irrelevant.<br />
I hope it will assist you well. <br />
You are welcome to leave comments and code contribution.<br />
<br />
RUN INFO:<br />
The project runs with configuration path as an argument. Configurtion is in Yaml format.<br />
Written on Python 2.7.<br />
Running file is Program.py. <br />
Run line example: C:\Users\MyUser\PycharmProjects\fb_scraper\Program.py "C:\Users\MyUser\configuration.yml"<br />
The Authentication information is in the configuration file to prevent it from being hard coded.<br />
Program module calls Orchestrator class which is the main class that orchestrate the program.<br />
<br />
PACKAGES:<br />
Pymongo<br />
PySide<br />
Bs4 (BeautifulSoup)<br />
Selenium<br />
<br /><br />
OUTPUT:<br />
The Output is an app UI table which shows selected posts.<br />
It shows the post content, enables to open the post in browesr, or mark it.<br />
When hovering over the post content column - the whole content is shown as tooltip.<br />
When marking irrelevant - it will later update it on DB.<br />
It is currently oriented for job serch, so iff an email address was found it can auto send my CV files with older module I wrote a few years ago (and on this git account as well).<br />
<br /><br />
KNOWN ISSUES:<br />
Most are documented within the code.<br />


