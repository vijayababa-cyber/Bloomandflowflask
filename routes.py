from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import BlogPost, User
from datetime import datetime
import re
import os
from werkzeug.utils import secure_filename

def is_valid_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/')
def index():
    """Main page route"""
    # Get featured blog posts for the homepage
    featured_posts = BlogPost.query.filter_by(published=True, featured=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('index.html', featured_posts=featured_posts)

@app.route('/blog')
def blog():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = BlogPost.query.filter_by(published=True)
    
    if category:
        query = query.filter_by(category=category)
    
    posts = query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False
    )
    
    # Get all categories for filter
    categories = db.session.query(BlogPost.category).filter_by(published=True).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('blog.html', posts=posts, categories=categories, current_category=category)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Get related posts from the same category
    related_posts = BlogPost.query.filter(
        BlogPost.category == post.category,
        BlogPost.id != post.id,
        BlogPost.published == True
    ).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
def new_blog_post():
    """Create new blog post (admin only)"""
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            summary = request.form.get('summary', '').strip()
            category = request.form.get('category', 'General').strip()
            tags = request.form.get('tags', '').strip()
            image_url = request.form.get('image_url', '').strip()
            featured = bool(request.form.get('featured'))
            published = bool(request.form.get('published'))
            
            # Generate slug from title
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
            slug = re.sub(r'\s+', '-', slug).strip('-')
            
            # Ensure slug is unique
            original_slug = slug
            counter = 1
            while BlogPost.query.filter_by(slug=slug).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Validation
            errors = []
            if not title:
                errors.append('Title is required')
            if not content:
                errors.append('Content is required')
            if not slug:
                errors.append('Could not generate valid URL from title')
            
            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                # Create new blog post
                post = BlogPost(
                    title=title,
                    content=content,
                    summary=summary,
                    category=category,
                    tags=tags,
                    image_url=image_url,
                    slug=slug,
                    featured=featured,
                    published=published
                )
                
                db.session.add(post)
                db.session.commit()
                
                flash('Blog post created successfully!', 'success')
                return redirect(url_for('blog_post', slug=slug))
                
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating blog post: {str(e)}")
            flash('An error occurred while creating the blog post. Please try again.', 'error')
    
    return render_template('admin/new_blog_post.html')

@app.route('/admin/blog')
def admin_blog():
    """Admin blog management page"""
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/blog_list.html', posts=posts)

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Name is required')
        elif len(name) < 2:
            errors.append('Name must be at least 2 characters long')
            
        if not email:
            errors.append('Email is required')
        elif not is_valid_email(email):
            errors.append('Please enter a valid email address')
            
        if not subject:
            errors.append('Subject is required')
        elif len(subject) < 3:
            errors.append('Subject must be at least 3 characters long')
            
        if not message:
            errors.append('Message is required')
        elif len(message) < 10:
            errors.append('Message must be at least 10 characters long')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # Log the contact form submission (in production, you'd send an email)
            app.logger.info(f"Contact form submission from {name} ({email}): {subject}")
            flash('Thank you for your message! We will get back to you soon.', 'success')
            
    except Exception as e:
        app.logger.error(f"Error processing contact form: {str(e)}")
        flash('An error occurred while sending your message. Please try again.', 'error')
    
    return redirect(url_for('index') + '#contact')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    flash('An internal error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500
