This tutorial shows how to manage JSON documents for the Redis Bike Co.

## Accessing Data Stored in JSON Documents

```redis Retrieve the entire document for a bike
JSON.GET redisbikeco:bike:rbc00001 $
```

```redis Get specific fields
JSON.GET redisbikeco:bike:rbc00001 $.stockcode $.specs.material
```

```redis Get a field from multiple documents
JSON.MGET redisbikeco:bike:rbc00001 redisbikeco:bike:rbc00002 $.brand
```

```redis Access elements of a JSON array
JSON.GET redisbikeco:store:ch $.amenities[0]
```
## Updating JSON Documents

```redis Update an existing value
JSON.SET redisbikeco:store:ch $.address.street '"Main Street"' 
```

```redis Add a new sub-object
JSON.SET redisbikeco:store:ch $.staff '{"manager": "Simon", "mechanic": "Savannah"}'
```

```redis Patch the staff object with JSON.MERGE
JSON.MERGE redisbikeco:store:ch $.staff '{"manager": "Justin", "mechanic": null, "cleaner": "Simon"}'
```

```redis Append an element to an array
JSON.ARRAPPEND redisbikeco:store:ch $.amenities '"creche"' 
```

```redis Reduce the price of a bike
JSON.NUMINCRBY redisbikeco:bike:rbc00001 $.price -100
```