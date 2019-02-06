#!/bin/bash -v

curl -O http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-4-amd64.deb
sudo dpkg -i couchbase-release-1.0-4-amd64.deb

sudo apt-get update -y
sudo apt install couchbase-server -y

sleep 10
/opt/couchbase/bin/couchbase-cli cluster-init --cluster-username Administrator --cluster-password password --services data,index,query,fts,analytics,eventing
