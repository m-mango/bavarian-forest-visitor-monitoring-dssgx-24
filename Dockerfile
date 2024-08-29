# Install Python base image
FROM python:3.10

# Create folder for source code and make it working directory
RUN mkdir -p /app
WORKDIR /app

# Install the python requirements
COPY Docker-requirements.txt .
RUN pip install -r Docker-requirements.txt

# Run pipeline and dashboard entry script
CMD ["streamlit", "run", "Main.py"]