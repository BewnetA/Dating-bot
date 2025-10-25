import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

def test_handler_import(handler_name):
    try:
        if handler_name == "start":
            from handlers.start import router
            print(f"✅ {handler_name} - SUCCESS")
            return True
        elif handler_name == "profile":
            from handlers.profile import router
            print(f"✅ {handler_name} - SUCCESS")
            return True
        elif handler_name == "matching":
            from handlers.matching import router
            print(f"✅ {handler_name} - SUCCESS")
            return True
        elif handler_name == "commands":
            from handlers.commands import router
            print(f"✅ {handler_name} - SUCCESS")
            return True
    except Exception as e:
        print(f"❌ {handler_name} - ERROR: {e}")
        return False

print("Testing handler imports...")
handlers = ["start", "profile", "matching", "commands"]
all_success = True

for handler in handlers:
    if not test_handler_import(handler):
        all_success = False

if all_success:
    print("\n🎉 All handlers imported successfully!")
else:
    print("\n💥 Some handlers failed to import!")