#!/usr/bin/env python3
"""
Build script to generate static HTML files for GitHub Pages deployment
"""

import os
import shutil
from app import app

def build_static():
    """Generate static HTML files from the Flask app"""
    
    # Create build directory
    build_dir = 'build'
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    # Generate static HTML
    with app.test_client() as client:
        # Get the main page
        response = client.get('/')
        
        # Save the HTML content
        with open(os.path.join(build_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(response.get_data(as_text=True))
    
    # Copy static files if they exist
    static_dir = 'static'
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, os.path.join(build_dir, 'static'))
    
    # Copy cards_data.json for client-side access
    if os.path.exists('cards_data.json'):
        shutil.copy('cards_data.json', os.path.join(build_dir, 'cards_data.json'))
    
    print("✅ Static build completed successfully!")
    print(f"📁 Files generated in: {build_dir}/")

if __name__ == '__main__':
    build_static() 