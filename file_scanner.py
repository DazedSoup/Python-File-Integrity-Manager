import os
import hashlib
import fnmatch

def is_ignored(filename):
    """
    Checks if a filename matches any of the ignore patterns.
    """
    ignore_patterns = [
        '*.tmp', '*.temp', '~$*', '*.bak', '__pycache__', 
        '.DS_Store', 'Thumbs.db'
    ]
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False

def calculate_hash(filepath):
    """
    Calculates the SHA-256 hash of a file.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read in chunks to handle large files efficiently
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (OSError, PermissionError):
        # In case we can't read the file (e.g. permission issues), we skip it or log it
        # For this module, we will return None to indicate failure
        return None

def scan_directory(directory_path):
    """
    Scans a directory recursively, ignores temp files, and returns 
    a dictionary of {filepath: sha256_hash}.
    """
    file_hashes = {}
    
    # Ensure we are working with an absolute path so results are absolute
    directory_path = os.path.abspath(directory_path)
    
    for root, dirs, files in os.walk(directory_path):
        # Modify dirs in-place to avoid traversing ignored directories like __pycache__
        dirs[:] = [d for d in dirs if not is_ignored(d)]
        
        for filename in files:
            if is_ignored(filename):
                continue
                
            filepath = os.path.join(root, filename)
            file_hash = calculate_hash(filepath)
            
            if file_hash:
                file_hashes[filepath] = file_hash
                
    return file_hashes

if __name__ == "__main__":
    # Example usage (for testing purposes)
    import sys
    
    target_dir = r"C:\Users\user\.gemini\antigravity\FIM project\test_files"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        
    print(f"Scanning directory: {target_dir}")
    results = scan_directory(target_dir)
    for path, h in results.items():
        print(f"{h}  {path}")
