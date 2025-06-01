# Bloom and Flow - Women's Period Hygiene Awareness Website

A responsive educational website built with Flask that provides comprehensive information about menstrual health and hygiene. Features a soft pink theme, blog functionality, and modern design.

## Features

- **Responsive Design**: Mobile-friendly layout with Bootstrap 5
- **Educational Content**: 
  - Hygiene tips section with practical guidance
  - Myths vs Facts section debunking misconceptions
  - FAQ section with accordion functionality
  - Doctor consultation warnings and suggestions
- **Blog System**: 
  - Admin interface for creating posts
  - Categories and tags
  - Featured posts on homepage
  - SEO-friendly URLs
- **Modern UI**: Soft pink theme with animations and smooth scrolling
- **Contact Form**: With validation and flash messages

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (with SQLite fallback)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5, Custom CSS with CSS custom properties
- **Icons**: Font Awesome, Custom SVG icons

## Installation

1. Clone or extract the project files
2. Install Python dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-login psycopg2-binary gunicorn werkzeug email-validator
   ```
3. Set environment variables:
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="postgresql://username:password@localhost/dbname"  # Optional, will use SQLite if not set
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Production Deployment

For production deployment:

1. Set environment variables properly
2. Use a proper WSGI server like Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
   ```
3. Configure a reverse proxy (nginx) for static files
4. Set up SSL/TLS certificates
5. Use a proper database (PostgreSQL recommended)

## File Structure

```
bloom-flow-website/
├── app.py                 # Flask application setup
├── main.py               # Entry point
├── models.py             # Database models
├── routes.py             # URL routes and handlers
├── pyproject.toml        # Python dependencies
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── images/           # SVG icons
└── templates/            # HTML templates
    ├── index.html        # Main page
    └── admin/            # Admin templates
        └── new_blog_post.html
```

## Blog Management

To add blog posts:

1. Navigate to `/admin/blog/new`
2. Fill in the blog post form
3. Set categories, tags, and featured status
4. Publish or save as draft

## Customization

- **Colors**: Modify CSS custom properties in `style.css`
- **Content**: Edit sections in `templates/index.html`
- **Styling**: Add custom styles in `static/css/style.css`
- **Icons**: Replace SVG files in `static/images/`

## Environment Variables

- `SESSION_SECRET`: Required for Flask sessions
- `DATABASE_URL`: PostgreSQL connection string (optional)

## License

This project is provided as-is for educational purposes.

## Support

For any issues or questions about the codebase, refer to the Flask and Bootstrap documentation.