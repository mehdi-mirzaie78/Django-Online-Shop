FROM python:3.11
LABEL Maintainer="markdownpro@gmail.com"
LABEL Version="V1.0.1"
WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Shop.wsgi"]
