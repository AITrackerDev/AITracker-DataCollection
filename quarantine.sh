#!/bin/bash

# remove qurantine attribute
remove_quarantine() {
    local file_or_dir="$1"
    
    # Check if the file/directory exists
    if [ -e "$file_or_dir" ]; then
        # Remove quarantine attribute
        xattr -d com.apple.quarantine "$file_or_dir" &> /dev/null
        
        # If it's a directory, recursively call this function for its contents
        if [ -d "$file_or_dir" ]; then
            for item in "$file_or_dir"/*; do
                remove_quarantine "$item"
            done
        fi
    else
        echo "File or directory not found: $file_or_dir"
    fi
}

# current directory
directory="$(pwd)"

# remove qurantine attribute for all files and directories
for item in "$directory"/*; do
    remove_quarantine "$item"
done

echo "Quarantine attributes have been removed from all files. The application is now able to be launched."

# self destruct script
rm -- "$0"