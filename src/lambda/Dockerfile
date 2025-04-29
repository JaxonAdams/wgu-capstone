# Use the official AWS Lambda Python 3.11 image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory to /var/task (Lambda's default code location)
WORKDIR /var/task

# Copy function code and dependencies
COPY predict.py ./
COPY requirements.txt ./

# Install dependencies into /var/task
RUN pip install -r requirements.txt --target .

# Set the Lambda function handler
CMD ["predict.handler"]