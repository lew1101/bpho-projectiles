# BPhO Computational Challenge 2024 Submission - Projectiles

The British Physics Olympiad (BPhO) Computational Challenge is a competition designed to test students' problem-solving abilities using computational methods. This year's computational challenge consists of a series of 9 progressively difficult tasks focused on the dynamics of projectiles.

Our submission is a website written completely using [`Streamlit`](https://streamlit.io/), an open-source app framework which allows us to easily write interactive web apps quickly and easily using only Python. The embedded interactive charts are generated using [`Plotly`](https://plotly.com/python/), a powerful open-source data visualization library.

## Cloning the Repo

Make sure you have [`git`](https://git-scm.com/) installed on your machine. Then, clone this repo using the following command:

```shell
git clone https://github.com/lew1101/projectiles-cc.git
```

## Installing Dependencies

This repo relies on [`poetry`](https://python-poetry.org/) for dependency management. Make sure it is installed on your machine, then run the following commands:

```shell
# start virtual environment
poetry shell

# install dependencies
poetry install 
```

## Running the Web App

```shell
streamlit run Home.py
```

## Authors

[Kenneth Lew](https://github.com/lew1101)
Timothy Ka
