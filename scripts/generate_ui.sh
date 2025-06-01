#!/bin/bash
# Script to generate Python code from .ui files

# Create the generated directory if it doesn't exist
mkdir -p ../app/ui/generated

# Convert all .ui files in the layouts directory to Python code
for ui_file in ../app/ui/layouts/*.ui; do
    # Get the filename without the path and extension
    filename=$(basename -- "$ui_file")
    filename="${filename%.*}"
    
    # Generate the Python code
    echo "Converting $ui_file to ${filename}_ui.py"
    pyuic5 -x "$ui_file" -o "../app/ui/generated/${filename}_ui.py"
done

echo "UI generation complete!"