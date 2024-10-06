# Define your environmental variables here; TODO: Update them if needed
BAYERN_CLOUD_API_KEY := $(shell echo $(BAYERN_CLOUD_API_KEY))
REPO_PATH := $(shell pwd)
AWS_ACCESS_KEY_ID := $(shell echo $(AWS_ACCESS_KEY_ID))
AWS_SECRET_ACCESS_KEY : $(shell echo $(AWS_SECRET_ACCESS_KEY))
IMAGE_NAME := bavarian-forest

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run \
		-v $(REPO_PATH):/app \
		-e BAYERN_CLOUD_API_KEY=$(BAYERN_CLOUD_API_KEY) \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-p 8501:8501 \
		-t $(IMAGE_NAME)

# Run the Docker container
bash:
	docker run \
		-v $(REPO_PATH):/app \
		-e BAYERN_CLOUD_API_KEY=$(BAYERN_CLOUD_API_KEY) \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-p 8501:8501 \
		-it --entrypoint /bin/bash $(IMAGE_NAME)

# Combined build and run
streamlit: build run

# Combined build and bash
container: build bash