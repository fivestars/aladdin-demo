FROM nginx:1.12-alpine

COPY /nginx/config/nginx.conf /etc/nginx/nginx.conf
