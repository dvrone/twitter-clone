from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Tweet, User
from app.forms import TweetForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def feed():
    form = TweetForm()
    if form.validate_on_submit():
        tweet = Tweet(body=form.body.data, user_id=current_user.id)
        db.session.add(tweet)
        db.session.commit()
        flash('Tweet posted!', 'success')
        return redirect(url_for('main.feed'))

    tweets = Tweet.query.order_by(Tweet.created_at.desc()).all()
    return render_template('main/feed.html', tweets=tweets, form=form)


@main_bp.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    tweets = user.tweets.order_by(Tweet.created_at.desc()).all()
    return render_template('main/profile.html', user=user, tweets=tweets)