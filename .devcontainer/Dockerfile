FROM python:3.12-slim

#WORKDIR /app

RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# upgradeing pip to the latest version
RUN pip install --upgrade pip
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# installation tools for building and publication a Python package
RUN pip install --no-cache-dir setuptools wheel twine

EXPOSE 8080

#COPY . .

CMD ["sleep", "infinity"]
