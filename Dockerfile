# Use the official Python image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy the entire project into the container
COPY bookmanager /app/

# Migrate database
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# Expose port 5000 for the Django app
EXPOSE 5000


# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]