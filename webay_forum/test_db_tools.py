"""This is a test for webay_forum/db_tools.py"""

from db_tools import UserDBTools, ForumDBTools

USERNAME = "UniqueUsername1"
NEW_USERNAME = "Miguel"
NEW_PASSWORD = "Not My Real Pass"

user_tools = UserDBTools()
user_tools.local = True
forum_tools = ForumDBTools()
forum_tools.local = True


user_added = user_tools.create_user(USERNAME, "FakePassword101")
user__id = user_tools.read_user(USERNAME)
user_updated = user_tools.update_user(user__id, new_user=NEW_USERNAME, new_pass=NEW_PASSWORD)
# user_deleted = user_tools.delete_user(user__id)
# print(F"User Added: {user_added}\nUser Updated: {user_updated}\nUser Deleted: {user_deleted}")

title = "A Root Post"

content = "This is the content of a root post. This post should not have a parent__id attribute."

orig__id = forum_tools.create_post(user__id, content, title=title)
post__id1 = forum_tools.create_post(user__id, content, title=title)
post__id2 = forum_tools.create_post(user__id, content, title=title)
post__id3 = forum_tools.create_post(user__id, "Just To Delete", parent__id=orig__id)
forum_tools.update_post(post__id1, title="This was post__id1")
forum_tools.update_post(post__id2, content="This was post__id2")
forum_tools.delete_post(post__id3)

if user_tools.login_user(USERNAME, "FakePassword101"):
    print("Login Successful!")
print(user_tools.all_users())