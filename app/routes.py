from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required

from app.models import URL, db, get_istanbul_time

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/shorten', methods=['POST'])
@login_required
def shorten():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL gerekli'}), 400

    url_obj = URL(
        original_url=url,
        user_id=current_user.id
    )
    db.session.add(url_obj)
    db.session.commit()

    short_url = request.host_url + url_obj.short_id
    created_at = url_obj.created_at.strftime('%Y-%m-%d %H:%M')
    
    return jsonify({
        'short_url': short_url,
        'original_url': url_obj.original_url,
        'clicks': url_obj.clicks,
        'created_at': created_at
    })

@main.route('/<short_id>')
def redirect_to_url(short_id):
    url = URL.query.filter_by(short_id=short_id).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@main.route('/urls')
@login_required
def url_list():
    urls = URL.query.filter_by(user_id=current_user.id).order_by(URL.created_at.desc()).all()
    return render_template('urls.html', urls=urls)

@main.route('/set-language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.home')) 