#!/bin/bash
cd /mnt/scala_projects/${PROJECT_NAME} && rm -rf project/META-INF/ && sbt clean cleanFiles && sbt compile && sbt package