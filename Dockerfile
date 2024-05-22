# Use an official Python runtime as a base image
FROM python:3.12

LABEL maintainer="Esteban Bobbiesi"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Build arguments
ARG ENV
ARG LOG_LEVEL

ENV ENV=${ENV}
ENV LOG_LEVEL=${LOG_LEVEL}
ENV PYTHONUNBUFFERED=0


WORKDIR /integration-tests

# Print environment variables to verify they are set correctly
RUN echo "ENVIRONMENT=$ENV"
RUN echo "LOG_LEVEL=$LOG_LEVEL"
RUN echo "CLEAN_LOGS=$CLEAN_LOGS"
RUN echo "APPLICATION=$APPLICATION"
RUN echo "TAG=$TAG"
RUN echo "NOT_RUN=$NOT_RUN"
RUN echo "TAG_BUG=$TAG_BUG"
RUN echo "PYTHONUNBUFFERED=$PYTHONUNBUFFERED"

COPY requirements.txt /integration-tests

# Create and activate virtual environment
RUN python -m venv .venv

# Use the virtual environment's pip to install dependencies
RUN . .venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Installs allure in the agent
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"
RUN brew install allure
RUN allure --version

COPY . /integration-tests

EXPOSE 8080

# Execution arguments
ARG TAG
ARG NOT_RUN
ARG TAG_BUG
ARG APPLICATION
ARG PLATFORM

CMD ["/bin/bash", "-c", ". .venv/bin/activate && python -m behave -D application=$APPLICATION -D platform=$PLATFORM -D log_level=$LOG_LEVEL --tags=\"$TAG\" --tags=\"$NOT_RUN\" --tags=\"$TAG_BUG\" --no-skipped && tail -f /dev/null"]


