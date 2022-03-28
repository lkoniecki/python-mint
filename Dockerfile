FROM python:slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY mint.py .
CMD [ "python3", "-u", "mint.py"]