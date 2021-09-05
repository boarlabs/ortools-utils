FROM sakha002/linprog-service:1.0-cbc-glpk

RUN pip3 install -r ./requirements.txt

WORKDIR  /
RUN mkdir linprog-service

COPY ./ ./linprog-service

CMD ["/bin/bash", "linprog-service/run-service.sh"]