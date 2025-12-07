FROM python:3.12.12-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ENV PYTHONPATH=/app

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip wheel

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./ ./

# RUN chmod +x ./entrypoint.sh

# ENTRYPOINT ["./entrypoint.sh"]

CMD ["python3", "app/main.py"]