#!/usr/bin/env python3
"""
Production-ready entry point for Bloom and Flow website
"""
import os
from app import app

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Check if we're in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )