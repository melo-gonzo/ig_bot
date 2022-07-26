from instapy import InstaPy
from instapy import smart_run
from login import *
import random
# get a session!
session = InstaPy(username=username, password=password)
# let's go! :>
with smart_run(session):

    session.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=False, max_followers=10000, max_following=100000000,
                                    min_followers=35, min_following=35)
    session.set_user_interact(amount=1, randomize=True, percentage=100, media='Photo')
    session.set_do_follow(enabled=True, percentage=100)
    session.set_do_like(enabled=True, percentage=100)
    # activity
    photo_comments = ['Nice shot! :thumbsup:',
                      'I love your profile!',
                      'Your feed is an inspiration :thumbsup:',
                      'Just incredible :open_mouth:',
                      'What camera did you use? :thumbsup:',
                      'Love your posts :thumbsup:',
                      'Looks awesome :thumbsup:',
                      'Getting inspired by you :thumbsup:',
                      ':raised_hands: Yes!',
                      'I can feel your passion :muscle:']
    session.set_comments(photo_comments, media='Photo')
    session.set_do_comment(enabled=True, percentage=100)
    session.unfollow_users(amount=75, nonFollowers=True, style="RANDOM", unfollow_after=42 * 60 * 60, sleep_delay=3)
    session.like_by_tags(
        random.shuffle(['photography', 'blackandwhitephotography', 'naturephotography', 'photographylovers', 'Instaphoto', 'photogram',
         'photographyislife', 'justgoshoot', 'picoftheday', 'photooftheday', 'love', 'nature',
         'sunset', 'sunrise', 'landscape', 'flowers', 'mountains', 'sky', 'lake', 'river', 'ocean',
         'instalike', 'love', 'instagood', 'fashion', 'beautiful', 'friends', 'summer', 'selfie', 'food',
         'family', 'igers', 'tbt', 'happy']), amount=10)
    session.join_pods(topic='general')
