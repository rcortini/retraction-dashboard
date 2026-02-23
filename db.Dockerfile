# db.Dockerfile
FROM postgres:16

# Optional: copy initialization SQL scripts
COPY ./db/init.sql /docker-entrypoint-initdb.d/init.sql

ENV POSTGRES_DB=openalex
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432