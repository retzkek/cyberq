FROM python:3
RUN pip install requests prometheus_client
COPY cyberq.py .
CMD ["python3","cyberq.py"]
