# Automated EBS Snapshots
FROM alpine:3.4

ADD requirements.txt ./

# Install python deps
RUN apk --update add python py-pip ca-certificates \
  && \
  pip install -r requirements.txt \
  && \
  rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

# Add application files
ADD . ./

# Run
CMD ["/usr/bin/python", "/main.py"]
