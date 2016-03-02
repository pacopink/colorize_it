# The FROM instruction sets the Base Image for subsequent instructions.
# Using Ubuntu as Base Image
FROM daocloud.io/library/python:2.7.11
RUN pip install flask
RUN mkdir /colorize_it
ADD ./ /colorize_it

EXPOSE 5050

CMD ["python", "/colorize_it/colorizer.py"]
