FROM gradiant/spark:2.4.4-python-alpine

COPY . /usr/src/pyspark/.

RUN pip install -r /usr/src/pyspark/requirements.txt

WORKDIR /usr/src/pyspark

CMD ["python3","/usr/src/pyspark/train_spark_mllib_model.py","." ]

