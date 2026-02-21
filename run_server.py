"""
Simple script to run the Flask server with output
"""
import sys
import os

print("="*60)
print("Starting AgriChem Solutions Backend Server")
print("="*60)

# Check if database exists
if not os.path.exists('agrichem.db'):
    print("\n✓ Creating new database...")
else:
    print("\n✓ Database already exists")

print("✓ Importing Flask app...")
from app import app, init_db, seed_data

# Initialize database if needed
if not os.path.exists('agrichem.db'):
    print("✓ Initializing database tables...")
    init_db()
    print("✓ Seeding initial data...")
    seed_data()

print("\n" + "="*60)
print("Server Configuration:")
print("="*60)
print("URL: http://localhost:5000")
print("Admin Dashboard: Open admin.html in browser")
print("API Docs: http://localhost:5000/")
print("="*60)
print("\nServer is running... Press Ctrl+C to stop\n")

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
