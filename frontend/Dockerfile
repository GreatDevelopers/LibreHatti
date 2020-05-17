FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
COPY ../scripts ./
EXPOSE 3000
CMD [ "npm", "run", "start" ]
