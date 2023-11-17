FROM python:3.10

ENV  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_HOME="/home/poetry" \
  VENV_PATH="/home/ecomm .venv" \
  USER="ecomm"

ENV  PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd $USER

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    ca-certificates \
    locales locales-all \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /home/$USER 
WORKDIR /home/$USER
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . ./
COPY --chown=$USER:$USER . .

RUN pip install --no-cache -U poetry

# Install pip separately
# RUN poetry run python -m pip install -U pip

# Set up the project and install dependencies
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry config virtualenvs.path .venv \
    && poetry install \
  #  && poetry run python -m pip install -U pip setuptools \
    && poetry lock



CMD ["poetry", "run", "python", "src/main.py"]
