# retrieve latest locust as wheels

1. `docker run -it -v $(pwd):/locustio python:3.6.2-slim bash`
2. `cd /locustio && apt-get update && apt-get install build-essential`
3. `pip3 wheel locustio`
4. `pip3 wheel psutil`
5. quit docker
6. Place all wheels in `src/locust`
7. Remove old locust wheel
8. Change in package call for locust with new version
