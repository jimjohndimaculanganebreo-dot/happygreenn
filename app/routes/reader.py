from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Novel, Chapter, LibraryItem, Comment

reader_bp = Blueprint("reader", __name__, url_prefix="/reader")

@reader_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("reader/dashboard.html", items=current_user.library_items)

@reader_bp.route("/profile", methods=["POST"])
@login_required
def update_profile():
    current_user.username = request.form["username"].strip()
    db.session.commit()
    flash("Profile updated.", "success")

    return redirect(url_for("reader.dashboard"))

@reader_bp.route("/library/add/<int:novel_id>", methods=["POST"])
@login_required
def add_to_library(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    item = LibraryItem.query.filter_by(
        user_id=current_user.id,
        novel_id=novel.id
    ).first()

    if not item:
        db.session.add(LibraryItem(user_id=current_user.id, novel_id=novel.id))
        db.session.commit()

    flash("Added to your library.", "success")

    return redirect(url_for("public.novel_detail", novel_id=novel.id))

@reader_bp.route("/progress", methods=["POST"])
@login_required
def save_progress():
    data = request.get_json()

    chapter = Chapter.query.get_or_404(int(data["chapter_id"]))

    item = LibraryItem.query.filter_by(
        user_id=current_user.id,
        novel_id=chapter.novel_id
    ).first()

    if not item:
        item = LibraryItem(user_id=current_user.id, novel_id=chapter.novel_id)
        db.session.add(item)

    item.current_chapter_id = chapter.id
    item.progress_percent = min(100, max(0, float(data.get("progress", 0))))

    db.session.commit()

    return jsonify({"ok": True})

@reader_bp.route("/comment/<int:chapter_id>", methods=["POST"])
@login_required
def add_comment(chapter_id):
    body = request.form["body"].strip()

    if body:
        db.session.add(Comment(
            user_id=current_user.id,
            chapter_id=chapter_id,
            body=body
        ))
        db.session.commit()

    return redirect(url_for("public.read_chapter", chapter_id=chapter_id))