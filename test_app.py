"""
Simple test script to verify our FastAPI application
"""

import sys
import os

def test_app():
    """Test if our FastAPI app is working"""
    print("🚀 Testing Receipt Processing API...")
    
    try:
        # Import and test the app directly
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from app.main import app
        
        # Test the app object
        print("✅ FastAPI app created successfully!")
        print(f"📋 App title: {app.title}")
        print(f"📋 App version: {app.version}")
        
        # List available routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(f"{route.methods} {route.path}")
        
        print(f"🔗 Available routes: {len(routes)}")
        for route in routes:
            print(f"   - {route}")
            
        print("\n🎉 Basic setup is working correctly!")
        print("📝 Next steps:")
        print("   1. Create database models")
        print("   2. Add file upload functionality")
        print("   3. Implement OCR processing")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_app()