from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_babel import _
from flask_login import current_user, login_required
from sqlalchemy import func

from app.firebase_config import get_firebase_config
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
    url = URL.query.filter_by(short_id=short_id, deleted_at=None).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@main.route('/urls')
@login_required
def url_list():
    urls = URL.query.filter_by(user_id=current_user.id, deleted_at=None).order_by(URL.created_at.desc()).all()
    return render_template('urls.html', urls=urls)

@main.route('/profile')
@login_required
def profile():
    """User profile page"""
    urls_count = URL.query.filter_by(user_id=current_user.id, deleted_at=None).count()
    clicks_count = db.session.query(func.sum(URL.clicks)).filter(URL.user_id == current_user.id, URL.deleted_at == None).scalar() or 0
    return render_template('profile.html', urls_count=urls_count, clicks_count=clicks_count)

@main.route('/url/delete/<int:id>', methods=['POST'])
@login_required
def delete_url(id):
    """Soft delete a URL"""
    url = URL.query.get_or_404(id)
    
    # Check if the URL belongs to the current user
    if url.user_id != current_user.id:
        flash(_('Bu işlem için yetkiniz yok.'), 'danger')
        return redirect(url_for('main.url_list'))
    
    # Soft delete
    url.deleted_at = get_istanbul_time()
    db.session.commit()
    
    flash(_('Link başarıyla silindi.'), 'success')
    return redirect(url_for('main.url_list'))

@main.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.home'))

@main.route('/api/firebase-config')
def firebase_config():
    """Return Firebase configuration for frontend"""
    config = get_firebase_config()
    return jsonify(config) 