import requests
import time
import os
from datetime import datetime

class WebsiteMonitor:
    def __init__(self, url, filename="website_content.txt", interval=300):
        self.url = url
        self.filename = filename
        self.interval = interval  # seconds
    
    def get_current_content(self):
        """Fetch current website content"""
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def load_previous_content(self):
        """Load previously saved content"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    return file.read()
            except IOError as e:
                print(f"Error reading file: {e}")
        return None
    
    def save_content(self, content):
        """Save content to file"""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(content)
            return True
        except IOError as e:
            print(f"Error saving file: {e}")
            return False
    
    def detect_changes(self):
        """Check for website changes"""
        current_content = self.get_current_content()
        if current_content is None:
            return False
        
        previous_content = self.load_previous_content()
        
        if previous_content is None:
            # First time - save initial content
            if self.save_content(current_content):
                print(f"[{datetime.now()}] Initial content saved.")
            return False
        
        if current_content != previous_content:
            print(f"[{datetime.now()}] CHANGE DETECTED!")
            print(f"Previous length: {len(previous_content)}")
            print(f"Current length: {len(current_content)}")
            
            # Save new content
            if self.save_content(current_content):
                print("New content saved.")
            
            # Here you can add notification logic
            # self.send_notification()
            
            return True
        else:
            print(f"[{datetime.now()}] No changes detected.")
            return False
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        print(f"Starting website monitoring for: {self.url}")
        print(f"Check interval: {self.interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                self.detect_changes()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")

# Usage example
if __name__ == "__main__":
    website_url = "https://httpbin.org/html"
    monitor = WebsiteMonitor(website_url, interval=60)  # Check every minute
    monitor.start_monitoring()