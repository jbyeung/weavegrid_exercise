FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
ADD . .
ADD /directoryAPI .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
COPY . .
CMD ["python", "./api.py"]