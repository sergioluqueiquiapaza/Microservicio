
from app.extensions import db
from datetime import datetime

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True) # ID único del token
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "jti": self.jti,
            "created_at": self.created_at
        }
