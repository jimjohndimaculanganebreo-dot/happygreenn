from datetime import datetime
from app.extensions import db


class Novel(db.Model):
    __tablename__ = "novels"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_url = db.Column(db.String(500), nullable=True)
    is_published = db.Column(db.Boolean, default=True)

    total_reads = db.Column(db.Integer, default=0)
    date_started = db.Column(db.Date, nullable=True)
    date_ended = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    chapters = db.relationship(
        "Chapter",
        back_populates="novel",
        cascade="all, delete-orphan",
        order_by="Chapter.chapter_number"
    )

    library_items = db.relationship(
        "LibraryItem",
        back_populates="novel",
        cascade="all, delete-orphan"
    )