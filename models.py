from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationship with blog posts
    blog_posts = db.relationship('BlogPost', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(300))
    image_url = db.Column(db.String(500))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    published = db.Column(db.Boolean, default=False)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to User
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Blog post categories
    category = db.Column(db.String(100), default='General')
    tags = db.Column(db.String(500))  # Comma-separated tags
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def formatted_date(self):
        """Return formatted date for display"""
        return self.created_at.strftime('%B %d, %Y')
    
    def reading_time(self):
        """Estimate reading time based on content length"""
        words = len(self.content.split())
        # Average reading speed is 200-250 words per minute
        minutes = max(1, words // 200)
        return f"{minutes} min read"