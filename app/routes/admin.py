from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Novel, Chapter
from werkzeug.utils import secure_filename
import os
import uuid

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


def save_cover_image(file):
    if not file or file.filename == "":
        return None

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]

    if ext not in allowed_extensions:
        flash("Invalid image type. Please upload JPG, PNG, or WEBP only.")
        return None

    unique_filename = f"{uuid.uuid4().hex}{ext}"

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    upload_path = os.path.join(upload_folder, unique_filename)
    file.save(upload_path)

    return f"/static/uploads/{unique_filename}"


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    novels = Novel.query.order_by(Novel.created_at.desc()).all()
    return render_template("admin/dashboard.html", novels=novels)


@admin_bp.route("/novel/new", methods=["GET", "POST"])
@login_required
@admin_required
def novel_form():
    novel = None

    if request.method == "POST":
        cover_file = request.files.get("cover")
        cover_url = save_cover_image(cover_file)

        novel = Novel(
            title=request.form["title"],
            description=request.form["description"],
            cover_url=cover_url,
            is_published=bool(request.form.get("is_published"))
        )

        db.session.add(novel)
        db.session.commit()

        flash("Novel created successfully.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/novel_form.html", novel=novel)


@admin_bp.route("/novel/<int:novel_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_novel(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    if request.method == "POST":
        cover_file = request.files.get("cover")
        new_cover_url = save_cover_image(cover_file)

        novel.title = request.form["title"]
        novel.description = request.form["description"]

        if new_cover_url:
            novel.cover_url = new_cover_url

        novel.is_published = bool(request.form.get("is_published"))

        db.session.commit()

        flash("Novel updated successfully.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/novel_form.html", novel=novel)


@admin_bp.route("/novel/<int:novel_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_novel(novel_id):
    db.session.delete(Novel.query.get_or_404(novel_id))
    db.session.commit()

    flash("Novel deleted successfully.")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/novel/<int:novel_id>/chapter/new", methods=["GET", "POST"])
@login_required
@admin_required
def chapter_form(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    chapter = None

    if request.method == "POST":
        chapter = Chapter(
            novel_id=novel.id,
            title=request.form["title"],
            chapter_number=int(request.form["chapter_number"]),
            content=request.form["content"],
            youtube_url=request.form.get("youtube_url"),
            is_published=bool(request.form.get("is_published"))
        )

        db.session.add(chapter)
        db.session.commit()

        flash("Chapter created successfully.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/chapter_form.html", novel=novel, chapter=chapter)


@admin_bp.route("/chapter/<int:chapter_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)

    if request.method == "POST":
        chapter.title = request.form["title"]
        chapter.chapter_number = int(request.form["chapter_number"])
        chapter.content = request.form["content"]
        chapter.youtube_url = request.form.get("youtube_url")
        chapter.is_published = bool(request.form.get("is_published"))

        db.session.commit()

        flash("Chapter updated successfully.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/chapter_form.html", novel=chapter.novel, chapter=chapter)


@admin_bp.route("/chapter/<int:chapter_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_chapter(chapter_id):
    db.session.delete(Chapter.query.get_or_404(chapter_id))
    db.session.commit()

    flash("Chapter deleted successfully.")
    return redirect(url_for("admin.dashboard"))