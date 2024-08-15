# Use Python 3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy your model, application, requirements, and static files into the container
COPY best_model ./best_model
COPY Dr-Tom.py ./Dr-Tom.py
COPY requirements.txt ./requirements.txt
COPY static ./static

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "Dr-Tom:app", "--host", "0.0.0.0", "--port", "8000"]
