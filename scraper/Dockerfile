FROM python:3.5

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools

RUN pip install numpy



# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

