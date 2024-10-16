![Bavarian Forest Logo](assets/logo-bavarian-forest-national-park.png)
# Harmonizing tourism and nature protection in the Bavarian Forest National Park 🌲 

This repository includes the code and documentation for the project "*Harmonizing tourism and nature protection in the Bavarian Forest National Park*" by [Data Science for Social Good Munich, 2024](https://sites.google.com/view/dssgx-munich-2023/startseite).

## Project Overview 🌍 

### Background 📜

The Bavarian Forest National Park is a protected area in the Bavarian Forest in Bavaria, Germany. Since its foundation, the park has been a place for nature conservation and research. The park is also a popular tourist destination, attracting visitors over 1.4 million visitors per year from all over the world. The park is home to a wide variety of flora and fauna, including many rare and endangered species.

### Problem Statement 🎯

The park faces the challenge of balancing the needs of nature conservation with the demands of tourism. The park has installed a network of sensors (26 visitor counters and 12 parking sensors) to understand the flow of visitors which will optimize the visitor experience and protect the park's natural resources. These data collected is heterogeneous and needs to be unified and harmonized to provide insights for decision-making.

### Project Goal and Contributions 🚀

The goal of this project is to harmonize the data collected from the sensors in the Bavarian Forest National Park to provide insights for decision-making. 
We contribute to the project in the following ways:
1. Develop a data pipeline to harmonize the data collected from the all the different sensors and external sources.
2. Implemented a predictive model to forecast the visitor traffic in the park for the coming weeks.
3. Develop a dashboard to visualize the data and insights for the park management, along with visualizing the forecasted visitor traffic from the predictive model.
4. Create a technical documentation to provide insights on the data pipeline, predictive model and suggestions for future improvements in the project.

![Overall Solution](assets/overall-dashboard.gif)
_Figure: Solution Dashboard_

## How to use the code 🛠️

### Option 1: Run code in a Docker container

1. Clone the repository:
   ```bash
   git clone https://github.com/DSSGxMunich/bavarian-forest-visitor-monitoring-dssgx-24.git
    ```
2. Download Docker Desktop from [here](https://www.docker.com/products/docker-desktop/) and install it.

3. Login to your AWS account with Single-Sign-On (SSO) and configure the AWS CLI with your credentials. Follow the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html).
    ```bash
    aws sso login --profile my-dev-aws-profile
    ```

3. Run the following command to build and run the streamlit dashboard.
   ```bash
   make streamlit
   ```
    [!NOTE]  If you want to run the bash shell in the docker container, run the following command:
    ```bash
    make container
    ```


### Option 2: Run code in a local a virtual environment

Choose a virtual environment of your choice and install the dependencies of the `requirements.txt` in the root of the repository. In the following, you see the steps to create a virtual environment with a particularly, specified Python version with `pyenv` and the plugin `pyenv-virtualenv`.

1.  Install `pyenv-virtualenv`. Follow a tutorial to install `pyenv` and the plugin `pyenv-virtualenv`, e.g. follow [this tutorial](https://medium.com/@adocquin/mastering-python-virtual-environments-with-pyenv-and-pyenv-virtualenv-c4e017c0b173).

2. Create a virtual environment with a specified Python version.
    ```bash
    pyenv virtualenv {selected-python-version} {name-of-virtual-environment}
    ```
3. Activate the virtual environment.
    ```bash
    pyenv activate {name-of-virtual-environment}
    ```
4. Install the dependencies of the `requirements.txt` in the root of the repository.
    ```bash
    pip install -r requirements.txt
    ```
## Structure of the repository 📁

The repository is structured as follows:

```
bavarian-forest-visitor-monitoring-dssgx-24/
│
├── assets/                 # Contains images and other assets for the README
│
├── data/                   # Contains the data used in the project
│
├── docs/                   # Contains the technical documentation
│
├── notebooks/              # Contains the notebooks for the data pipeline and predictive model
│
├── src/                    # Contains the source code for the data pipeline and predictive model
│
├── pages/                  # Contains the additional pages for the streamlit dashboard
│
├── Makefile                # Contains the commands to run the code
│
├── README.md               # Contains the information about the project
│
├── requirements.txt        # Contains the dependencies of the project
│
└── Dashboard.py            # Contains the code for the calling the predictive model and the streamlit dashboard
```

## Technical Documentation 📚

The technical documentation website is available [here](https://dssgxmunich.github.io/bavarian-forest-visitor-monitoring-dssgx-24/). 

## How to contribute to the project 🤝

Follow the following steps to contribute to the project:

1. Fork the repository to your GitHub account.
2. Create a new branch with a descriptive name for the feature you want to contribute to.
3. Make changes to the code or documentation.
4. Commit the changes to your branch.
5. Push the changes to your forked repository.
6. Create a pull request to the main repository.

NOTE: Be sure to merge the latest from the `upstream` before making a pull request!

### Requesting new features or reporting bugs 🐞

If you have any suggestions for new features or find any bugs, please create an issue in the repository.

Feel free to submit issues and enhancement requests. We are open to feedback and contributions!

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


