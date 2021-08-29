FROM linprog-service:1.0-cbc-glpk

RUN pip3 install grpcio grpcio-tools

WORKDIR  /
RUN mkdir linprog-service

COPY ./ ./linprog-service

CMD ["/bin/bash", "linprog-service/run-service.sh"]