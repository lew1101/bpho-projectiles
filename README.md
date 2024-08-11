# BPhO Computational Challenge 2024 Submission - Projectiles

The British Physics Olympiad (BPhO) Computational Challenge is a competition designed to test students' problem-solving abilities using computational methods. This year's computational challenge consists of a series of 9 progressively difficult tasks focused on the dynamics of projectiles. The instructions and mathematical derivations provided by BPhO for each of the challenges can be found [here](./res/instructions).

Our submission is a website written completely using [`Streamlit`](https://streamlit.io/), an open-source app framework which allows us to easily write interactive web apps quickly and easily using only Python. The embedded interactive charts are generated using [`Plotly`](https://plotly.com/python/), a powerful open-source data visualization library.

## Cloning the Repo

Make sure you have [`git`](https://git-scm.com/) installed on your machine. Then, clone this repo using the following command:

```shell
git clone https://github.com/lew1101/bpho-projectiles.git && cd bpho-projectiles
```

## Installing Dependencies

This repo relies on [`poetry`](https://python-poetry.org/) for dependency management. Make sure it is installed on your machine, then run the following command to install dependencies:

```shell
poetry install 
```

## Running the Web App using Streamlit

```shell
# initialize virtual env (not necessary if using pip without venv)
source ./venv/bin/activate

# initiate server (another port could be used)
streamlit run app.py --server.port 8501
```

## Alternative: Deploying using Docker

First, clone the repo. Then, make sure you have the [`Docker`](https://docs.docker.com/) client and daemon installed. Ensure the daemon is started, then build the image:

```shell
docker build --tag bp-image .
```

To run a container, first set the `PORT` environment variable to the desired port for the server to listen to. The environment variable can also be passed using the `--env (-e)` flag, for example:

```shell
docker run --env PORT=8501 --publish 8501:8501 bp-image
```

## Authors

[Kenneth Lew](https://github.com/lew1101)

[Timothy Ka](https://github.com/TimothyKa100)
