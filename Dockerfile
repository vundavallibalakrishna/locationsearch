FROM python:3.6.10-stretch
ADD . ./app/
WORKDIR /app/
RUN python -m pip install --upgrade pip && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
#ENV FLASK_APP "./server.py"
#ENV FLASK_DEBUG True
ENV APP_CONFIG_FILE=./config/production.py
EXPOSE 5000
#CMD flask run --host=0.0.0.0
ENTRYPOINT [ "python" ]
CMD [ "server.py" ]
