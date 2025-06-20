# 1. Use an official, slim Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container first
# This is a Docker caching optimization. It avoids reinstalling packages on every code change.
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port the app will run on
EXPOSE 8050

# 7. Define the command to run the application using Gunicorn (a production server)
# This runs the 'server' object from the 'app.py' file.
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8050"]