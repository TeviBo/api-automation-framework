
# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app


EXPOSE 8080


ARG ENVIRONMENT=qa
ARG TAGS=REGRESSION
ARG LOG_LEVEL=INFO
ARG CLEAN_LOGS=False
ARG CONSOLE_HANDLER=True
ARG APPLICATION=JKR
ARG NOT_RUN=NOT_MRK
ARG TAG_BUG=FAIL
ARG SKIP_TAG=~NOT_LIM014


# Run behave when the container launches
CMD python -m behave --no-skipped --tags=$TAGS \
                                            -D environment=$ENVIRONMENT \
                                            -D log_level=$LOG_LEVEL \
                                            -D console_handler=$CONSOLE_HANDLER \
                                            -D clean_logs=$CLEAN_LOGS \
                                            -D console_handler=$CONSOLE_HANDLER \
                                            -D application=$APPLICATION \
                                            --tags=$NOT_RUN \
                                            --tags=$TAG_BUG \
                                            --tags=$SKIP_TAG