This tutorial shows how to query JSON documents for the Redis Bike Co.

## Querying JSON Documents

Which aluminium bikes weigh between 5 and 10kg?:

```redis Aluminium Bikes 5-10kg
FT.SEARCH idx:bikes "@material:{aluminium} @weight:[5 10]" RETURN 4 stockcode brand model weight LIMIT 0 3 SORTBY weight ASC
```

Which kids bikes cost less than 10,000 Rupees?

```redis Kids Bikes in Price Range
FT.SEARCH idx:bikes "@type:{Kids Bikes} @price:[-inf 9999]" return 3 brand model price
```

What different types of bike are there?

```redis Types of Bike
127.0.0.1:6379> ft.aggregate idx:bikes "*" groupby 1 @type
```

Which road bikes are either carbon or full-carbon?

```redis Carbon or Full-Carbon
FT.SEARCH idx:bikes "@type:{Road Bikes} @material:{carbon|full\\-carbon}"
```

Which bikes are comfortable, but not made of aluminium or alloy?

```redis Comfortable bikes
FT.SEARCH idx:bikes "@description:comfortable -@material:{aluminium|alloy}"
```

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