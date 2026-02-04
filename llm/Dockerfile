FROM ollama/ollama

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/startup.sh"]
