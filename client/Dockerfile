# Pull official base image
FROM node:alpine

# Set working directory
WORKDIR /app/client

# Install dependencies
COPY ./package.json .
COPY ./package-lock.json .

RUN npm install

# Add /node_modules/.bin to $PATH
ENV PATH ./node_modules/.bin:$PATH

# Copy code
COPY . .

# Start app
CMD ["npm", "start"]
