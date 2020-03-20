"""This is a test for webay_forum/db_tools.py"""

from db_tools import UserDBTools


db_tools = UserDBTools()
db_tools.local = True

db_tools.add_user("UniqueUsername!", "FakePassword101")
