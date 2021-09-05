FROM sakha002/linprog-service:1.0-cbc-glpk


WORKDIR  /
RUN mkdir linprog-service

COPY ./ ./linprog-service

RUN pip3 install -r /linprog-service/requirements.txt

CMD ["/bin/bash", "linprog-service/run-service.sh"]