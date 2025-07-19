import serial
import time
import json
import atexit
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variable to hold the serial connection
arduino = None

def connect_to_arduino(port='COM9', baudrate=9600, max_retries=3):
    """Connect to Arduino with retry logic"""
    global arduino
    
    # Close existing connection if it exists
    if arduino and arduino.is_open:
        arduino.close()
        time.sleep(1)
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to Arduino on {port}... (attempt {attempt + 1})")
            arduino = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Give Arduino time to initialize
            print(f"Successfully connected to Arduino on {port}")
            return True
        except serial.SerialException as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
            else:
                print("Warning: Arduino not connected. Will attempt to reconnect on first request.")
                return False
    return False

def ensure_connection():
    """Ensure Arduino connection is active"""
    global arduino
    if arduino is None or not arduino.is_open:
        return connect_to_arduino()
    return True

def cleanup():
    """Clean up serial connection"""
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        print("Serial connection closed")

# Register cleanup function
atexit.register(cleanup)

@app.route('/test', methods=['POST'])
def test():
    """Test endpoint"""
    return jsonify({"status": "success", "message": "Bridge is working!"})

@app.route('/display', methods=['POST'])
def display():
    """Send message to Arduino LCD"""
    global arduino
    
    try:
        # Get the message from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data['message']
        
        # Ensure connection is active
        if not ensure_connection():
            return jsonify({"error": "Failed to connect to Arduino"}), 500
        
        # Send message to Arduino
        arduino.write(f"{message}\n".encode())
        arduino.flush()
        
        # Optional: Wait for acknowledgment from Arduino
        time.sleep(0.1)
        response = ""
        if arduino.in_waiting:
            response = arduino.readline().decode().strip()
        
        return jsonify({
            "status": "success", 
            "message": f"Sent: {message}",
            "arduino_response": response
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Check Arduino connection status"""
    global arduino
    connected = arduino is not None and arduino.is_open
    return jsonify({
        "arduino_connected": connected,
        "port": "COM9" if connected else "Not connected"
    })

if __name__ == '__main__':
    print("Starting Arduino LCD Bridge...")
    
    # Initial connection attempt
    connect_to_arduino()
    
    print("Bridge is ready!")
    print("Test endpoint: POST http://localhost:5000/test")
    print("Display endpoint: POST http://localhost:5000/display")
    print("Status endpoint: GET http://localhost:5000/status")
    
    # Run Flask app without debug mode to prevent auto-restart
    app.run(host='0.0.0.0', port=5000, debug=False)
