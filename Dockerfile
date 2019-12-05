FROM python:3.6.9-alpine3.9
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py .
COPY boot.sh .
COPY templates templates
EXPOSE 5000
RUN chmod +x boot.sh
ENTRYPOINT [ "./boot.sh" ]