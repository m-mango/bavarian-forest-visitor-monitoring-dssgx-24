# bavarian-forest-visitor-monitoring-dssgx-24
This repo includes the code developed during DSSGx Munich 2024 for a project that supports the Bavarian Forest with their project to monitor and manage visitors of the Bavarian Forest.

## How to run the code

### Run the pipeline and dashboard via Docker container

1. Install Docker to your local machine. Follow tutorials/guidelines online.

2. Verify the Docker installation:

```
docker --version
```

3. Initiate the Docker Engine (e.g., start the Docker app).

4. Navigate to the root of the repository. Build a Docker container for our project with the following command:

```
docker build -t bavarian-forest .
```

5. In the meantime, log into your AWS account:

In case you have not yet configured AWS locally on your machine, make sure to set it up (see Slack or ping TM Julie).

```
aws sso login
```


5. After the Docker container has been built, run the Docker container with attaching the repository and aws credentials as volume (`-v` parameter) and specify the AWS role you assume with the following command:

```
docker run -v {path-to-repo}:/app -v {path-to-aws-credentials-folder}/.aws:/root/.aws -e AWS_PROFILE={name-of-your-aws-profile} -p 8501:8501 -t bavarian-forest
```

Optional:

In order to not use the entrypoint specified in the `Dockerfile`, run the Docker container in bash mode to jump into the terminal of the Docker (more flexibility for execution):

```
docker run -it --entrypoint /bin/bash bavarian-forest
```


### Create a virtual environment

Choose a virtual environment of your choice and install the dependencies of the `requirements.txt` in the root of the repository. In the following, you see the steps to create a virtual environment with a particularly, specified Python version with `pyenv` and the plugin `pyenv-virtualenv`.

#### Install pyenv-virtualenv

Follow a tutorial to install `pyenv` and the plugin `pyenv-virtualenv`, e.g. follow [this tutorial](https://medium.com/@adocquin/mastering-python-virtual-environments-with-pyenv-and-pyenv-virtualenv-c4e017c0b173).

#### Create virtual environment with specified Python version

Adjust and run the following command in the CLI:

```
pyenv virtualenv {selected-python-version} {name-of-virtual-environment}
```

As an example: 

```
pyenv virtualenv 3.10.13 iom-migration-foresight-dssgx-24
```

#### Active the virtual environment

Adjust and run the following command in the CLI:

```
pyenv activate {name-of-virtual-environment}
```

As an example: 

```
pyenv activate iom-migration-foresight-dssgx-24
```

#### Install needed dependencies

Best case, the `requirements.txt` in the root of the repository is up-to-date and contains all necessary dependencies to run the code contained in the repository.

To install the needed dependencies to be used in the virtual environment, run the following command in the CLI:

```
pip install -r requirements.txt
```

### Run Jupyter Notebooks

#### Install `jupyter` 

Either you have already added the `jupyter` library as dependecy to the `requirements.txt` or you still need to do it and install it in your virtual environment.

#### Add the virtual environment as Jupyter kernel

In order to be able to run Jupyter notebooks in the created virtual environment, you need to specify a new kernel to be used by Jupyter making use of your virtual environment. Run the following command in the CLI by specifying a name for the kernel:

```
python -m ipykernel install --user --name={name-for-kernel}
```

#### Open Jupyter notebook

Either run the following command in the CLI to trigger the pop-up of the Jupyter interface in your browser:

```
jupyter notebook
```

OR: In case you are keen on using Jupyter Notebooks in the IDE VS Code, open the Jupyter Notebook in VS Code. (Tip: this way you can use all other VS Code features in notebooks, for example nice code highlighting, AI Coding features, etc.)

#### Select kernel

In both the Jupyter UI and the notebook in VS Code, you need to select the specified kernel from before running the cells.

#### Run the notebook

Now go ahead and run the notebook! :)
