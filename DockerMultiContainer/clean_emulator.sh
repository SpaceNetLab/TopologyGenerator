#!/bin/bash
#build the constellation of starlink, where 1584 satellites into 72 orbital planes of 22 satellites each
ORBIT_NUM=72
SATELLITE_PER_ORBIT=22

for i in `seq 1 $ORBIT_NUM`;
do
  ORBIT_INDEX=`expr $i - 1`
  DOCKER_YML_PATH="starlink/orbit_$ORBIT_INDEX"
  echo $DOCKER_YML_PATH
  cd $DOCKER_YML_PATH
  pwd
  docker-compose down
  cd ../..
done