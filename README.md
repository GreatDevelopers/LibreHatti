LibreHatti
==========

Raising Pull Request
--------------------
- Always raise PR from fork or new branch.
- Run pre-commit hooks locally. Follow instructions to install pre-commit. Pre checks will run automatically with `git commit`


**Install Pre-commit**

```
cd LibreHatti
pip3 install pre-commit
pre-commit install
```
- Make sure PR have proper title and description
- Link project to the PR
- Add proper labels
- Link tickets to PR

Setting up Environment
------------------------
Since we use docker environment, it is quite easy setup your local environment
1. [Install](https://docs.docker.com/engine/install/) docker
2. `cd Librehatti`
3. To run web app, use `docker-compose run web`
4. To run api and react UI, use `docker-compose run frontend`
