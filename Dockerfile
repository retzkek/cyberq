FROM python:3
COPY cyberq.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python3","cyberq.py"]
