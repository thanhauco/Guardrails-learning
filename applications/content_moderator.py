"""
Content Moderator Application
=============================

Batch processing script to moderate content in files.
Reads text files, checks for toxicity/PII, and writes clean versions.
"""

import os
import sys
import glob

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intermediate.toxic_content_detection import ToxicDetector
from intermediate.pii_detection import PIIDetector

class ContentModerator:
    def __init__(self):
        self.toxic_detector = ToxicDetector()
        self.pii_detector = PIIDetector()

    def process_file(self, input_path: str, output_path: str):
        print(f"Processing {input_path}...")
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Check Toxicity
            if self.toxic_detector.check(content).value == "toxic":
                print(f"  [Warning] Toxic content detected. Sanitizing...")
                content = self.toxic_detector.sanitize(content)

            # 2. Check PII
            if self.pii_detector.check(content).value == "found":
                print(f"  [Warning] PII detected. Redacting...")
                content = self.pii_detector.redact(content)

            # Write output
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved to {output_path}")

        except Exception as e:
            print(f"  [Error] Failed to process file: {e}")

    def batch_process(self, input_dir: str, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        files = glob.glob(os.path.join(input_dir, "*.txt"))
        print(f"Found {len(files)} files in {input_dir}")

        for file_path in files:
            filename = os.path.basename(file_path)
            out_path = os.path.join(output_dir, filename)
            self.process_file(file_path, out_path)

if __name__ == "__main__":
    # Create dummy data for demonstration
    os.makedirs("data/input", exist_ok=True)
    with open("data/input/sample1.txt", "w") as f:
        f.write("Hello, my email is john@example.com and I hate you.")
    
    moderator = ContentModerator()
    moderator.batch_process("data/input", "data/output")
    
    # Show result
    if os.path.exists("data/output/sample1.txt"):
        with open("data/output/sample1.txt", "r") as f:
            print("\n--- Result ---")
            print(f.read())
