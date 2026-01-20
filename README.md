# RAW Organizer

A Python tool to organize RAW and JPG files by removing orphaned files that don't have corresponding matches.

## Features

- **File Discovery**: Automatically finds all JPG and RAW files in a directory
- **Flexible Anchoring**: Choose to anchor on JPG files or RAW files
- **Smart Matching**: Matches files based on base filename (without extension)
- **Safe Operation**: Dry-run mode by default to preview changes
- **Comprehensive Reporting**: Shows detailed results of the organization process

## Supported File Types

### JPG Files
- `.jpg`
- `.jpeg`

### RAW Files
- `.cr2`, `.cr3` (Canon)
- `.nef` (Nikon)
- `.arw` (Sony)
- `.dng` (Adobe Digital Negative)
- `.orf` (Olympus)
- `.rw2` (Panasonic)
- `.pef` (Pentax)
- `.srw` (Samsung)
- `.x3f` (Sigma)

## Usage

### Basic Usage (Dry Run)
```bash
python raw_organizer.py /path/to/photos
```

### Anchor on JPG files (default)
```bash
python raw_organizer.py /path/to/photos --anchor jpg
```

### Anchor on RAW files
```bash
python raw_organizer.py /path/to/photos --anchor raw
```

### Actually delete files (use with caution!)
```bash
python raw_organizer.py /path/to/photos --execute
```

### Command Line Options

- `directory`: Input directory to organize (required)
- `--anchor {jpg,raw}`: File type to use as anchor (default: jpg)
- `--dry-run`: Perform a dry run without deleting files (default)
- `--execute`: Actually delete files (overrides --dry-run)

## How It Works

1. **Discovery**: Scans the specified directory for all JPG and RAW files
2. **Anchoring**: Uses the specified file type (JPG or RAW) as the "anchor"
3. **Matching**: Finds target files that have matching base names with anchor files
4. **Cleanup**: Identifies and optionally deletes orphaned files (files without matches)
5. **Reporting**: Provides a comprehensive report of the organization results

## Example Scenarios

### Scenario 1: Anchor on JPG files
- Directory contains: `IMG_001.jpg`, `IMG_002.jpg`, `IMG_001.cr2`, `IMG_003.cr2`
- Result: `IMG_003.cr2` is orphaned (no matching JPG) and will be deleted

### Scenario 2: Anchor on RAW files
- Directory contains: `IMG_001.jpg`, `IMG_002.jpg`, `IMG_001.cr2`, `IMG_003.cr2`
- Result: `IMG_002.jpg` is orphaned (no matching RAW) and will be deleted

## Safety Features

- **Dry Run by Default**: Never deletes files unless explicitly requested
- **Confirmation Prompt**: Asks for confirmation before deleting files
- **Detailed Reporting**: Shows exactly which files will be/were deleted
- **Error Handling**: Gracefully handles file access errors

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Installation

1. Clone or download the repository
2. No additional installation required - just run the script!

```bash
python raw_organizer.py --help
```

## Example Output

```
Scanning directory: /path/to/photos
Found 25 JPG files
Found 20 RAW files

Organizing with JPG files as anchor...
Anchor files: 25
Target files: 20

Found 3 orphaned RAW files:
  - /path/to/photos/IMG_999.cr2
  - /path/to/photos/DSC_1234.nef
  - /path/to/photos/untitled.arw

[DRY RUN] Would delete 3 orphaned RAW files

============================================================
ORGANIZATION REPORT
============================================================
Anchor files (JPG): 25
Target files (RAW): 20
Orphaned files found: 3
Files deleted: 0

Orphaned RAW files:
  - /path/to/photos/IMG_999.cr2
  - /path/to/photos/DSC_1234.nef
  - /path/to/photos/untitled.arw

Deleted files:
(none - dry run mode)

============================================================
```

## License

This project is open source and available under the MIT License.
