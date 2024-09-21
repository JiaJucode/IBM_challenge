FROM python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# copy the rest of the files to workdir/backend fodlder for consistency
COPY . .
CMD ["python", "app.py"]
