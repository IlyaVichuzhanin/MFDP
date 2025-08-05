# Use the official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy the application code to the working directory
#COPY . .

# # Expose the port on which the application will run
 EXPOSE 9090


# Run the FastAPI application using uvicorn server
CMD ["python", "main.py"]