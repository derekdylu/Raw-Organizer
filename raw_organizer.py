#!/usr/bin/env python3
"""
RAW Organizer - A tool to organize RAW files based on matching JPG files
or vice versa, removing orphaned files that don't have corresponding matches.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Set, Tuple
import re


class RawOrganizer:
    def __init__(self, input_directory: str):
        self.input_directory = Path(input_directory)
        if not self.input_directory.exists():
            raise FileNotFoundError(f"Directory {input_directory} does not exist")
        
        self.jpg_files = []
        self.raw_files = []
        self.deleted_files = []
        
        # Common RAW file extensions
        self.raw_extensions = {'.cr2', '.cr3', '.nef', '.arw', '.dng', '.orf', '.rw2', '.pef', '.srw', '.x3f'}
        
    def discover_files(self) -> Tuple[List[Path], List[Path]]:
        """Discover all JPG and RAW files in the directory."""
        print(f"Scanning directory: {self.input_directory}")
        
        jpg_files = []
        raw_files = []
        
        for file_path in self.input_directory.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in ['.jpg', '.jpeg']:
                    jpg_files.append(file_path)
                elif ext in self.raw_extensions:
                    raw_files.append(file_path)
        
        self.jpg_files = jpg_files
        self.raw_files = raw_files
        
        print(f"Found {len(jpg_files)} JPG files")
        print(f"Found {len(raw_files)} RAW files")
        
        return jpg_files, raw_files
    
    def get_base_name(self, file_path: Path) -> str:
        """Extract base name without extension for matching."""
        return file_path.stem
    
    def find_matches(self, anchor_files: List[Path], target_files: List[Path]) -> Set[str]:
        """Find which target files have matching anchor files."""
        anchor_base_names = {self.get_base_name(f) for f in anchor_files}
        matching_targets = set()
        
        for target_file in target_files:
            target_base = self.get_base_name(target_file)
            if target_base in anchor_base_names:
                matching_targets.add(target_base)
        
        return matching_targets
    
    def find_orphaned_files(self, anchor_files: List[Path], target_files: List[Path]) -> List[Path]:
        """Find target files that don't have matching anchor files."""
        matching_bases = self.find_matches(anchor_files, target_files)
        orphaned = []
        
        for target_file in target_files:
            target_base = self.get_base_name(target_file)
            if target_base not in matching_bases:
                orphaned.append(target_file)
        
        return orphaned
    
    def delete_files(self, files_to_delete: List[Path], dry_run: bool = True) -> List[Path]:
        """Delete files with optional dry run."""
        deleted_files = []
        
        for file_path in files_to_delete:
            try:
                if not dry_run:
                    file_path.unlink()
                    deleted_files.append(file_path)
                    print(f"Deleted: {file_path}")
                else:
                    print(f"[DRY RUN] Would delete: {file_path}")
                    deleted_files.append(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        
        return deleted_files
    
    def organize_files(self, anchor_type: str, dry_run: bool = True) -> dict:
        """Main organization logic."""
        if anchor_type.lower() == 'jpg':
            anchor_files = self.jpg_files
            target_files = self.raw_files
            anchor_name = "JPG"
            target_name = "RAW"
        elif anchor_type.lower() == 'raw':
            anchor_files = self.raw_files
            target_files = self.jpg_files
            anchor_name = "RAW"
            target_name = "JPG"
        else:
            raise ValueError("Anchor type must be 'jpg' or 'raw'")
        
        print(f"\nOrganizing with {anchor_name} files as anchor...")
        print(f"Anchor files: {len(anchor_files)}")
        print(f"Target files: {len(target_files)}")
        
        # Find orphaned files
        orphaned_files = self.find_orphaned_files(anchor_files, target_files)
        
        print(f"\nFound {len(orphaned_files)} orphaned {target_name} files:")
        for file_path in orphaned_files:
            print(f"  - {file_path}")
        
        if orphaned_files:
            if dry_run:
                print(f"\n[DRY RUN] Would delete {len(orphaned_files)} orphaned {target_name} files")
            else:
                print(f"\nDeleting {len(orphaned_files)} orphaned {target_name} files...")
                deleted_files = self.delete_files(orphaned_files, dry_run=False)
                self.deleted_files.extend(deleted_files)
        
        return {
            'anchor_files': anchor_files,
            'target_files': target_files,
            'orphaned_files': orphaned_files,
            'deleted_files': self.deleted_files,
            'anchor_type': anchor_name,
            'target_type': target_name
        }
    
    def print_organization_report(self, results: dict):
        """Print comprehensive organization report."""
        print("\n" + "="*60)
        print("ORGANIZATION REPORT")
        print("="*60)
        
        print(f"Anchor files ({results['anchor_type']}): {len(results['anchor_files'])}")
        print(f"Target files ({results['target_type']}): {len(results['target_files'])}")
        print(f"Orphaned files found: {len(results['orphaned_files'])}")
        print(f"Files deleted: {len(results['deleted_files'])}")
        
        if results['orphaned_files']:
            print(f"\nOrphaned {results['target_type']} files:")
            for file_path in results['orphaned_files']:
                print(f"  - {file_path}")
        
        if results['deleted_files']:
            print(f"\nDeleted files:")
            for file_path in results['deleted_files']:
                print(f"  - {file_path}")
        
        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Organize RAW and JPG files by removing orphaned files')
    parser.add_argument('directory', help='Input directory to organize')
    parser.add_argument('--anchor', choices=['jpg', 'raw'], default='jpg',
                       help='File type to use as anchor (default: jpg)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Perform a dry run without actually deleting files')
    parser.add_argument('--execute', action='store_true',
                       help='Actually delete files (overrides --dry-run)')
    
    args = parser.parse_args()
    
    try:
        # Initialize organizer
        organizer = RawOrganizer(args.directory)
        
        # Discover files
        jpg_files, raw_files = organizer.discover_files()
        
        if not jpg_files and not raw_files:
            print("No JPG or RAW files found in the directory.")
            return
        
        # Determine if we should actually delete files
        dry_run = not args.execute
        
        if dry_run:
            print("\n[DRY RUN MODE] - No files will be deleted")
            print("Use --execute flag to actually delete files")
        else:
            print("\n[EXECUTION MODE] - Files will be deleted!")
            response = input("Are you sure you want to proceed? (yes/no): ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                return
        
        # Organize files
        results = organizer.organize_files(args.anchor, dry_run)
        
        # Print report
        organizer.print_organization_report(results)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
