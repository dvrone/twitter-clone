from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


likes = db.Table(
    "likes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("tweet_id", db.Integer, db.ForeignKey("tweets.id"), primary_key=True),
)

follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(160), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tweets = db.relationship(
        "Tweet", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    liked_tweets = db.relationship(
        "Tweet",
        secondary=likes,
        backref=db.backref("liked_by", lazy="dynamic"),
        lazy="dynamic",
    )

    followed = db.relationship(
        "User",
        secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def like(self, tweet):
        if not self.has_liked(tweet):
            self.liked_tweets.append(tweet)

    def unlike(self, tweet):
        if self.has_liked(tweet):
            self.liked_tweets.remove(tweet)

    def has_liked(self, tweet):
        return self.liked_tweets.filter(Tweet.id == tweet.id).count() > 0

    def follow(self, user):
        if not self.is_following(user) and user.id != self.id:
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(follows.c.followed_id == user.id).count() > 0

    def __repr__(self):
        return f"<User {self.username}>"


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Tweet {self.id} by user {self.user_id}>"
