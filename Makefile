# Define your environmental variables here; TODO: Update them if needed
BAYERN_CLOUD_API_KEY := $(shell echo $(BAYERN_CLOUD_API_KEY))
REPO_PATH := $(shell pwd)
PATH_TO_STREAMLIT_SECRETS := ~/.streamlit/secrets.toml
IMAGE_NAME := bavarian-forest

# If using AWS SSO, update these variables
AWS_CREDENTIALS_PATH := ~/.aws
AWS_PROFILE := TM-DSSGx

# If using AWS permanent access key (for applications), update these variables
AWS_ACCESS_KEY_ID := $(shell echo $(AWS_ACCESS_KEY_ID))
AWS_SECRET_ACCESS_KEY : $(shell echo $(AWS_SECRET_ACCESS_KEY))

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run \
		-v $(REPO_PATH):/app \
		-v $(PATH_TO_STREAMLIT_SECRETS):/app/.streamlit/secrets.toml \
		-e BAYERN_CLOUD_API_KEY=$(BAYERN_CLOUD_API_KEY) \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-p 8501:8501 \
		-t $(IMAGE_NAME)

# Run the Docker container
bash:
	docker run \
		-v $(REPO_PATH):/app \
		-v $(PATH_TO_STREAMLIT_SECRETS):/app/.streamlit/secrets.toml \
		-e BAYERN_CLOUD_API_KEY=$(BAYERN_CLOUD_API_KEY) \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-p 8501:8501 \
		-it --entrypoint /bin/bash $(IMAGE_NAME)

sso-bash:
	docker run \
		-v $(REPO_PATH):/app \
		-v $(PATH_TO_STREAMLIT_SECRETS):/app/.streamlit/secrets.toml \
		-v $(AWS_CREDENTIALS_PATH):/root/.aws \
		-e BAYERN_CLOUD_API_KEY=$(BAYERN_CLOUD_API_KEY) \
		-e AWS_PROFILE=$(AWS_PROFILE) \
		-p 8501:8501 \
		-it --entrypoint /bin/bash $(IMAGE_NAME)

# Combined build and run
streamlit: build run

# Combined build and bash
container: build bash

# Combined build and sso-bash
sso-container: build sso-bash