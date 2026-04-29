from instapy import InstaPy

session = InstaPy(username="your username",password="your password")
session.login()


#liking post
session.like_by_tags(["dance", "mercedes"], amount=10, interact=True)

# dontlike
session.set_dont_like(["naked", "murder", "nsfw"])

#follow
session.set_do_comment(True, percentage=100)
session.set_comments(["Nice", "Amazing", "Super"])

# interaction
session.set_user_interact(amount=1, randomize=True, percentage=100)

# end session
session.end()
