FROM python:slim

#Set workdir
WORKDIR /app

#Copy app files
COPY app/ .

# Install dependencies
RUN pip install -r requirements.txt

#Expose the port
EXPOSE 5000

CMD ["flask", "run"]





