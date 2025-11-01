FROM python:3.13
WORKDIR /FastAPI-Cloud_crud
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "uvicorn","app.app:app","--reload" ]