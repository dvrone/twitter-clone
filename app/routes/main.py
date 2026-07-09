from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Tweet

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def feed():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).all()
    return render_template('main/feed.html', tweets=tweets)