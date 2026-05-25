from datetime import datetime
from app.extensions import db

class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey("novels.id"), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    youtube_url = db.Column(db.String(500), nullable=True)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    novel = db.relationship("Novel", back_populates="chapters")
    comments = db.relationship("Comment", back_populates="chapter", cascade="all, delete-orphan")