FROM nginx:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY frontend /usr/share/nginx/html
COPY public /usr/share/nginx/html
COPY covers /opt/playnext/covers

RUN chmod -R a+rX /usr/share/nginx/html /opt/playnext/covers
