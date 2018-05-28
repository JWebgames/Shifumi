FROM python:3.6
ADD . /code
WORKDIR /code
EXPOSE 22451
CMD ["python", "server.py"]
