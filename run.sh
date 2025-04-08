#!/bin/bash

# Install dependencies if needed
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt file..."
    cat > requirements.txt << EOF
fastapi==0.95.1
uvicorn==0.22.0
jinja2==3.1.2
pandas==2.0.1
numpy==1.24.3
python-multipart==0.0.6
apscheduler==3.10.1
pydantic==1.10.7
EOF
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create a dummy "user.png" file if it doesn't exist
mkdir -p static/img
if [ ! -f "static/img/user.png" ]; then
    echo "Creating placeholder user avatar..."
    touch static/img/user.png
fi

# Create placeholder avatar images
for i in {1..5}; do
    if [ ! -f "static/img/avatar_$i.png" ]; then
        touch "static/img/avatar_$i.png"
    fi
done

# Run the application
echo "Starting the application..."
uvicorn app:app --host 0.0.0.0 --port 8000 --reload