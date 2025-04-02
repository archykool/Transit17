from datetime import datetime
from backend import db

class BaseModel(db.Model):
    """Base model class with common fields and methods"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def get_by_id(cls, id):
        """Get instance by id"""
        return cls.query.get(id)

    def save(self):
        """Save instance to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete instance from database"""
        db.session.delete(self)
        db.session.commit() 