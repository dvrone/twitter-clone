from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.forms import EditProfileForm, TweetForm
from app.models import Tweet, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
@login_required
def feed():
    form = TweetForm()
    if form.validate_on_submit():
        tweet = Tweet(body=form.body.data, user_id=current_user.id)
        db.session.add(tweet)
        db.session.commit()
        flash("Tweet posted!", "success")
        return redirect(url_for("main.feed"))

    followed_ids = [u.id for u in current_user.followed]
    followed_ids.append(current_user.id)

    tweets = (
        Tweet.query.filter(Tweet.user_id.in_(followed_ids))
        .order_by(Tweet.created_at.desc())
        .all()
    )

    suggestions = (
        User.query.filter(~User.id.in_(followed_ids))
        .order_by(func.random())
        .limit(5)
        .all()
    )

    return render_template(
        "main/feed.html", tweets=tweets, form=form, suggestions=suggestions
    )


@main_bp.route("/user/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    tweets = user.tweets.order_by(Tweet.created_at.desc()).all()
    return render_template("main/profile.html", user=user, tweets=tweets)


@main_bp.route("/tweet/<int:tweet_id>/like", methods=["POST"])
@login_required
def like_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    current_user.like(tweet)
    db.session.commit()
    return redirect(request.referrer or url_for("main.feed"))


@main_bp.route("/tweet/<int:tweet_id>/unlike", methods=["POST"])
@login_required
def unlike_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    current_user.unlike(tweet)
    db.session.commit()
    return redirect(request.referrer or url_for("main.feed"))


@main_bp.route("/user/<username>/follow", methods=["POST"])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.id == current_user.id:
        flash("You can't follow yourself.", "warning")
    else:
        current_user.follow(user)
        db.session.commit()
        flash(f"You are now following @{user.username}.", "success")
    return redirect(request.referrer or url_for("main.profile", username=username))


@main_bp.route("/user/<username>/unfollow", methods=["POST"])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You unfollowed @{user.username}.", "info")
    return redirect(request.referrer or url_for("main.profile", username=username))


@main_bp.route("/tweet/<int:tweet_id>/delete", methods=["POST"])
@login_required
def delete_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)

    if tweet.user_id != current_user.id:
        abort(403)

    db.session.delete(tweet)
    db.session.commit()
    flash("Tweet deleted.", "info")
    return redirect(request.referrer or url_for("main.feed"))


@main_bp.route("/settings/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("main.profile", username=current_user.username))

    return render_template("main/edit_profile.html", form=form)


@main_bp.route("/explore")
@login_required
def explore():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).all()
    return render_template("main/explore.html", tweets=tweets)
