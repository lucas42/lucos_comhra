FROM ollama/ollama
ARG VERSION
ENV VERSION=$VERSION

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh
COPY Modelfile /Modelfile

ENTRYPOINT ["/bin/sh"]
CMD ["/startup.sh"]
