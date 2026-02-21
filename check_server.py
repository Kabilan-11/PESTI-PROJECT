import socket
import time

def check_port(host='localhost', port=5000):
    """Check if port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

print("Checking if Flask server is running on port 5000...")
time.sleep(2)

if check_port():
    print("✓ Server is running on http://localhost:5000")
    print("\nYou can now:")
    print("1. Open pest1.html in your browser")
    print("2. Open admin.html to view the admin dashboard")
    print("3. Test the API endpoints")
else:
    print("✗ Server is not responding on port 5000")
    print("The server may still be starting up. Please wait a few seconds and try again.")
