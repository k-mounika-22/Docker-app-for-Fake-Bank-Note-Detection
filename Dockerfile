FROM continuumio/anaconda3
COPY . /usr/app/
EXPOSE 8501
WORKDIR /usr/app/
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
