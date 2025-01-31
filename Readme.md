﻿# Blog-Platform
Deployment Guide - Actual Commands
1. How to Build and Run the Project Locally Using Docker Compose
Prerequisites:
Ensure Docker and Docker Compose are installed on your system.

Steps to Run the Project Locally
Clone the repository (if not done already):

bash
Copy code
git clone <repository_url>
cd <project_directory>
Navigate to the project folder where the docker-compose.yml file is located:

bash
Copy code
cd /path/to/your/project/directory
Build and start the services using Docker Compose:

bash
Copy code
docker-compose up --build -d
Verify that the containers are running:

bash
Copy code
docker ps
Test the application locally by using curl:

bash
Copy code
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}' http://localhost:5000/login
2. How to Deploy the Project to AWS
Prerequisites:
An AWS account and EC2 instance with appropriate security group settings to allow traffic on port 5000 (or your desired port).
Steps to Deploy on AWS
Launch an EC2 instance (Ubuntu or Amazon Linux).

SSH into the EC2 Instance:

bash
Copy code
ssh -i "C:\Users\Anurag\Desktop\lembda.pem" ec2-user@ec2-52-66-240-107.ap-south-1.compute.amazonaws.com
Install Docker and Docker Compose on EC2:

bash
Copy code
sudo yum install docker -y   # For Amazon Linux
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
Transfer the Project Files to EC2:

bash
Copy code
scp -i "C:\Users\Anurag\Desktop\lembda.pem" -r /path/to/your/project/directory ec2-user@ec2-52-66-240-107.ap-south-1.compute.amazonaws.com:/home/ec2-user
Navigate to the Project Directory on EC2:

bash
Copy code
cd /home/ec2-user/Blog\ Platform
Build and Start the Docker Containers:

bash
Copy code
docker-compose up --build -d
Verify the Application is Running:

bash
Copy code
docker ps
Access the Application: Open your browser and visit the public IP of your EC2 instance on the appropriate port:

arduino
Copy code
http://52.66.240.107:5000
3. Live Deployment
Public URL for Deployed Application
Once deployed, the application should be accessible via:

arduino
Copy code
http://52.66.240.107:5000
To secure the URL with HTTPS:

Install Certbot:

bash
Copy code
sudo yum install certbot
Obtain SSL Certificate with Certbot:

bash
Copy code
sudo certbot certonly --standalone -d <your_domain>
Configure Nginx for HTTPS (optional for reverse proxy setup).

4. API Documentation
4.1 Register Endpoint
URL: /register/
Method: POST
Body:
json
Copy code
{
  "username": "testuser",
  "password": "password123"
}
Response:
Success: 200 OK
json
Copy code
{ "message": "User registered successfully" }
Failure: 400 Bad Request
json
Copy code
{ "message": "Username and password are required" }
4.2 Login Endpoint
URL: /login/
Method: POST
Body:
json
Copy code
{
  "username": "testuser",
  "password": "password123"
}
Response:
Success: 200 OK
json
Copy code
{ "message": "Login successful" }
Failure: 401 Unauthorized
json
Copy code
{ "message": "Invalid credentials" }
5. Trade-offs and Design Decisions
Database Choice
SQLite is used for simplicity in local development.
Trade-off: Not suitable for large-scale applications. In production, PostgreSQL or MySQL would be better.
Security
Passwords are hashed using werkzeug.security.generate_password_hash.
Trade-off: No advanced session management (e.g., JWT or OAuth2). Consider adding token-based authentication for production.
Docker Compose for Local Development
Docker Compose is used for containerizing the application, simplifying local development and ensuring all services run together.
This document contains the full set of commands for building, running, and deploying the project, as well as details about the live deployment and API documentation.






