This tutorial shows how to query JSON documents for the Redis Bike Co.

## Querying JSON Documents

Which aluminium bikes weigh between 5 and 10kg?:

```redis Aluminium Bikes 5-10kg
FT.SEARCH idx:bikes "@material:{aluminium} @weight:[5 10]" RETURN 4 stockcode brand model weight LIMIT 0 3 SORTBY weight ASC
```

Which kids bikes cost less than 10,000 Rupees?

```redis Kids Bikes in Price Range
FT.SEARCH idx:bikes "@type:{Kids Bikes} @price:[-inf 9999]" RETURN 3 brand model price
```

What different types of bike are there?

```redis Types of Bike
FT.AGGREGATE idx:bikes "*" GROUPBY 1 @type
```

Which road bikes are either carbon or full-carbon?

```redis Carbon or Full-Carbon
FT.SEARCH idx:bikes "@type:{Road Bikes} @material:{carbon|full\\-carbon}"
```

Which bikes are comfortable, but not made of aluminium or alloy?

```redis Comfortable bikes
FT.SEARCH idx:bikes "@description:comfortable -@material:{aluminium|alloy}"
```

Add a new field and update the index...

```redis Add New Field
JSON.MSET redisbikeco:bike:rbc00013 $.thumbsup 2 redisbikeco:bike:rbc00034 $.thumbsup 3 redisbikeco:bike:rbc00099 $.thumbsup 1
```

```redis Amend Bikes Index
FT.ALTER idx:bikes schema add $.thumbsup as thumbsup NUMERIC SORTABLE
```

Query the new field:

```redis Query thumbs up
FT.SEARCH idx:bikes "@thumbsup:[0 +inf]" RETURN 3 brand model thumbsup SORTBY thumbsup DESC
```

Which stores provide parking and rent bikes to customers?

```redis Parking and Rentals
FT.SEARCH idx:stores "@amenities:{parking} @amenities:{rentals}"
```

Which stores are within 100km of Lucknow?

```redis Stores near Lucknow
FT.SEARCH idx:stores "@position:[80.8599399 26.848668 100 km]" RETURN 2 storecode city
```
