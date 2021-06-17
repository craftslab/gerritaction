FROM python:3.9.0 as build-stage
WORKDIR /usr/src/app
COPY . .
RUN apt update && \
    apt install -y upx
RUN make install

FROM nginx as production-stage
WORKDIR /usr/dist/bin
RUN mkdir -p /usr/dist/bin
COPY --from=build-stage /usr/src/app/dist/* ./
COPY --from=build-stage /usr/src/app/gerritaction/config/*.yml ./
