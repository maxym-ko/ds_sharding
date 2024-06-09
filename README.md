## Run instructions

#### Step 1: Start MongoDB service
```shell
brew services start mongodb-community
```

#### Step 2: Create directories for logs, configs and shards
```shell
mkdir -p ./mongo/config
mkdir -p ./mongo/shard1 ./mongo/shard2
mkdir -p ./mongo/logs
```

#### Step 3: Start Config Server
```shell
mongod --configsvr --replSet configReplSet --dbpath ./mongo/config --port 27019 --logpath ./mongo/logs/config.log --fork
```

#### Step 4: Connect to the Config Server and initiate the Replica Set
```shell
mongosh --port 27019

rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "localhost:27019" }]
});
.exit
```

#### Step 5: Start Shard Servers
```shell
mongod --shardsvr --replSet shard1ReplSet --dbpath ./mongo/shard1 --port 27015 --logpath ./mongo/logs/shard1.log --fork
mongod --shardsvr --replSet shard2ReplSet --dbpath ./mongo/shard2 --port 27016 --logpath ./mongo/logs/shard2.log --fork
```

#### Step 6: Connect to Shard1 and Shard2 Servers and initiate the Replica Set
```shell
mongosh --port 27015

rs.initiate({
  _id: "shard1ReplSet",
  members: [{ _id: 0, host: "localhost:27015" }]
});
.exit
```
```shell
mongosh --port 27016

rs.initiate({
  _id: "shard2ReplSet",
  members: [{ _id: 0, host: "localhost:27016" }]
});
.exit
```

#### Step 7: Start mongos (the interface between the client applications and the sharded cluster)
```shell
mongos --configdb configReplSet/localhost:27019 --logpath ./mongo/logs/mongos.log --fork --port 27020
```

#### Step 8: Add Shards to the Cluster and Enable Sharding on a Database
```shell
mongosh --port 27020

sh.addShard("shard1ReplSet/localhost:27015");
sh.addShard("shard2ReplSet/localhost:27016");
```

#### Step 9: Enable Sharding on a Database
```
sh.enableSharding("testDatabase");

sh.shardCollection("testDatabase.users", { _id: "hashed" });

sh.status();
```

#### Step 10: Insert some documents
```
use testDatabase;
for (let i = 0; i < 1000; i++) {
  db.users.insertOne({ _id: i, name: "user" + i });
}

sh.status();
.exit
```

#### Step 10: Make sure documents are stored in both shards
```shell
mongosh --port 27015
use testDatabase;
db.users.countDocuments();  // Check shard1
.exit
```

```shell
mongosh --port 27016
use testDatabase;
db.users.countDocuments();  // Check shard2
.exit
```

#### Step 11: Simple check via Python client
```shell
pip install -r requirements.txt
python simple_check.py
```