#!/usr/bin/env python3
"""
Max Cognitive Shield - Desensitization Script
Automated sensitive data detection and replacement for open-source publication
"""

import os
import re
import json
import hashlib
import csv
from datetime import datetime
from pathlib import Path

class DesensitizationEngine:
    def __init__(self, mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.sensitive_patterns = self.config['sensitive_patterns']
        self.file_exclusions = self.config['file_exclusions']
        self.scan_directories = self.config['scan_directories']

        # Compile regex patterns for efficiency
        self.compiled_patterns = {}
        for category, data in self.sensitive_patterns.items():
            patterns = []
            for pattern in data['patterns']:
                try:
                    patterns.append(re.compile(pattern, re.IGNORECASE | re.UNICODE))
                except re.error:
                    # Handle invalid regex patterns
                    patterns.append(re.compile(re.escape(pattern), re.IGNORECASE | re.UNICODE))
            self.compiled_patterns[category] = {
                'patterns': patterns,
                'replacement': data['replacement'],
                'category': data['category']
            }

        self.report_data = []

    def should_skip_file(self, file_path):
        """Check if file should be excluded from scanning"""
        file_str = str(file_path).lower()
        for exclusion in self.file_exclusions:
            if exclusion.lower() in file_str:
                return True
        return False

    def calculate_hash(self, content):
        """Calculate SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def scan_and_replace_file(self, file_path):
        """Scan a single file and replace sensitive content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            modified_content = original_content
            file_changes = []

            # Apply all pattern replacements
            for category, pattern_data in self.compiled_patterns.items():
                for pattern in pattern_data['patterns']:
                    matches = list(pattern.finditer(modified_content))
                    if matches:
                        for match in matches:
                            original_text = match.group()
                            replacement = pattern_data['replacement']

                            # Replace in content
                            modified_content = modified_content.replace(original_text, replacement)

                            # Record change
                            file_changes.append({
                                'category': category,
                                'original_hash': self.calculate_hash(original_text),
                                'replacement': replacement,
                                'position': match.start()
                            })

            # Write back if changes were made
            if modified_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)

                # Record in report
                for change in file_changes:
                    self.report_data.append({
                        'file_path': str(file_path),
                        'sensitive_type': change['category'],
                        'processing_method': 'replacement',
                        'replacement_value_hash': change['original_hash'],
                        'operation_time': datetime.now().isoformat(),
                        'operator': 'automated_desensitization'
                    })

                return len(file_changes)

            return 0

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0

    def scan_directory(self, base_path):
        """Recursively scan directory for files to process"""
        total_files = 0
        total_changes = 0

        for scan_dir in self.scan_directories:
            dir_path = Path(base_path) / scan_dir
            if not dir_path.exists():
                continue

            for root, dirs, files in os.walk(dir_path):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not self.should_skip_file(d)]

                for file in files:
                    file_path = Path(root) / file

                    # Skip if file should be excluded
                    if self.should_skip_file(file_path):
                        continue

                    # Only process text-based files
                    if file_path.suffix.lower() in ['.py', '.js', '.ts', '.json', '.md', '.txt', '.yml', '.yaml', '.dockerfile', '']:
                        changes = self.scan_and_replace_file(file_path)
                        if changes > 0:
                            print(f"Processed {file_path}: {changes} changes")
                            total_changes += changes
                        total_files += 1

        return total_files, total_changes

    def generate_report(self, output_file):
        """Generate CSV report of all changes"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if self.report_data:
                writer = csv.DictWriter(f, fieldnames=self.report_data[0].keys())
                writer.writeheader()
                writer.writerows(self.report_data)

        print(f"Desensitization report generated: {output_file}")

    def run(self, base_path):
        """Main execution method"""
        print("Starting desensitization process...")
        print(f"Base path: {base_path}")

        total_files, total_changes = self.scan_directory(base_path)

        print(f"\nDesensitization completed:")
        print(f"Files processed: {total_files}")
        print(f"Total changes made: {total_changes}")

        # Generate report
        report_file = Path(base_path) / "desensitization_report.csv"
        self.generate_report(report_file)

        return total_files, total_changes

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python desensitize.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    mapping_file = "desensitization_mapping.json"

    engine = DesensitizationEngine(mapping_file)
    engine.run(project_path)