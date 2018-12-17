FROM ruby:2.4-alpine3.6

RUN apk --no-cache update
RUN apk --no-cache add ca-certificates build-base curl jq python py-pip py-setuptools python-dev
RUN pip --no-cache-dir install awscli
RUN gem install bundler
RUN mkdir /website
WORKDIR /website

COPY Gemfile Gemfile.lock ./
RUN bundle
COPY . .
