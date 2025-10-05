#!/usr/bin/env python3
import http.server
import socketserver
import threading
import time
import urllib.request
import json
import os

def start_server():
    """Start HTTP server in background"""
    os.chdir(r"c:\Users\MY LENOVO LOQ\Documents\Projects\handwriting detection")
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8080), handler) as httpd:
        print("Server started at http://localhost:8080")
        httpd.serve_forever()

def test_model_loading():
    """Test if all model components are accessible"""
    print("🔍 Testing Model Loading in index.html\n")
    
    base_url = "http://localhost:8080"
    
    # Test files
    test_files = [
        ("/", "index.html"),
        ("/cnn_model.js", "CNN Model JavaScript"),
        ("/models/model.json", "Model Architecture"),
        ("/models/weights.bin", "Model Weights")
    ]
    
    all_passed = True
    
    for path, description in test_files:
        try:
            response = urllib.request.urlopen(f"{base_url}{path}")
            status = response.getcode()
            if status == 200:
                print(f"✅ {description}: Accessible (Status: {status})")
                if path == "/":
                    # Check index.html content
                    content = response.read().decode('utf-8')
                    if 'cnnModel.loadModel()' in content:
                        print("  ✅ Model loading code found")
                    if 'id="modelStatus"' in content:
                        print("  ✅ Model status element found") 
                    if '@tensorflow/tfjs' in content:
                        print("  ✅ TensorFlow.js CDN found")
                elif path == "/models/model.json":
                    # Validate model.json structure
                    content = response.read().decode('utf-8')
                    model_data = json.loads(content)
                    if 'modelTopology' in model_data and 'weightsManifest' in model_data:
                        print("  ✅ Valid TensorFlow.js model format")
            else:
                print(f"❌ {description}: Status {status}")
                all_passed = False
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")
            all_passed = False
    
    # Check model files exist locally
    print(f"\n📁 Local File Verification:")
    local_files = [
        "index.html",
        "cnn_model.js", 
        "models/model.json",
        "models/weights.bin"
    ]
    
    for file_path in local_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path}: {size:,} bytes")
        else:
            print(f"❌ {file_path}: Not found")
            all_passed = False
    
    print(f"\n🎯 Overall Status: {'✅ PASS' if all_passed else '❌ FAIL'}")
    print(f"🚀 Ready to use: {'Yes' if all_passed else 'No'}")
    
    if all_passed:
        print("\n📋 Usage Instructions:")
        print("1. Open browser to http://localhost:8080")
        print("2. Wait for 'Model loaded successfully!' message")
        print("3. Draw a digit (0-9) on the canvas")
        print("4. Click 'Predict with CNN' button")
        print("5. See prediction results with confidence scores")

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Run tests
    test_model_loading()