FROM python:3.9.9-slim
WORKDIR /app
ADD . /app
RUN pip install flask
EXPOSE 5000
ENV NAME demo
CMD ["python","app-demo.py"]
