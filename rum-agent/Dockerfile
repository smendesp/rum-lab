# Use a specific Node.js base image (e.g., node:20-alpine for smaller size)
FROM node:20-alpine AS builder

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

RUN npm run build


# Final Scratch Stage
FROM nginx:stable-alpine3.21-perl

COPY --from=builder /usr/src/app/dist/rum-bundle.js /usr/share/nginx/html

EXPOSE 80

#CMD ["sleep", "infinity"]