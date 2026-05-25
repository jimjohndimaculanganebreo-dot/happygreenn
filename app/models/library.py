from datetime import datetime
from app.extensions import db

class LibraryItem(db.Model):
    __tablename__ = "library_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey("novels.id"), nullable=False)
    current_chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=True)
    progress_percent = db.Column(db.Float, default=0)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="library_items")
    novel = db.relationship("Novel", back_populates="library_items")
    current_chapter = db.relationship("Chapter")

    __table_args__ = (
        db.UniqueConstraint("user_id", "novel_id", name="unique_user_novel"),
    )