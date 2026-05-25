from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from app.extensions import db
from app.models import Novel, Chapter, LibraryItem

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    search = request.args.get("search", "").strip()

    if search:
        novels = Novel.query.filter(
            Novel.is_published == True,
            Novel.title.ilike(f"%{search}%")
        ).order_by(Novel.created_at.desc()).all()
    else:
        novels = Novel.query.filter_by(
            is_published=True
        ).order_by(Novel.created_at.desc()).all()

    return render_template("index.html", novels=novels, search=search)


@public_bp.route("/novel/<int:novel_id>")
def novel_detail(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    chapters = Chapter.query.filter_by(
        novel_id=novel.id,
        is_published=True
    ).order_by(Chapter.chapter_number).all()

    library_item = None

    if current_user.is_authenticated:
        library_item = LibraryItem.query.filter_by(
            user_id=current_user.id,
            novel_id=novel.id
        ).first()

    return render_template(
        "novel_detail.html",
        novel=novel,
        chapters=chapters,
        library_item=library_item
    )


@public_bp.route("/read/<int:chapter_id>")
def read_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)

    if not chapter.is_published:
        abort(404)

    novel = chapter.novel

    # total reads tracker
    novel.total_reads = (novel.total_reads or 0) + 1

    # continue reading tracker
    if current_user.is_authenticated:
        library_item = LibraryItem.query.filter_by(
            user_id=current_user.id,
            novel_id=novel.id
        ).first()

        if library_item:
            library_item.current_chapter_id = chapter.id

    db.session.commit()

    chapters = Chapter.query.filter_by(
        novel_id=novel.id,
        is_published=True
    ).order_by(Chapter.chapter_number).all()

    return render_template(
        "reader/read.html",
        chapter=chapter,
        chapters=chapters
    )