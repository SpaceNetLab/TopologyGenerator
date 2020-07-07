#!/bin/bash
#build the constellation of starlink, where 1584 satellites into 72 orbital planes of 22 satellites each
ORBIT_NUM=1584
SATELLITE_PER_ORBIT=1

ulimit -n 4096
export COMPOSE_HTTP_TIMEOUT=180
export COMPOSE_PARALLEL_LIMIT=2048

docker network create -d bridge star_bridge_0
docker network create -d bridge star_bridge_1
docker network create -d bridge star_bridge_2

#generate doecker compose files
python build_script.py

for i in `seq 1 $ORBIT_NUM`;
do
  ORBIT_INDEX=`expr $i - 1`
  DOCKER_YML_PATH="starlink/orbit_$ORBIT_INDEX"
  echo $DOCKER_YML_PATH
  cd $DOCKER_YML_PATH
  pwd
  docker-compose up -d
  cd ../..
done

