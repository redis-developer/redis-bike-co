# Redis Bike Company Example Application

TODO README!

```
poetry run python data_loader.py
```

INDEX CREATION COMMANDS:

Stores index:

```
FT.CREATE idx:stores ON JSON PREFIX 1 redisbikeco:store: SCHEMA $.storecode AS storecode TAG $.storename AS storename TAG $.address.city AS city TAG $.address.state AS state TAG $.address.pin AS pin TAG $.address.country AS country TAG $.position AS position GEO
```

Bikes index:

```
FT.CREATE idx:bikes ON JSON PREFIX 1 redisbikeco:bike: SCHEMA $.stockcode AS stockcode TAG SORTABLE $.model AS model TAG SORTABLE $.brand AS brand TAG SORTABLE $.type as type TAG SORTABLE $.description AS description TEXT $.specs.material AS material TAG SORTABLE $.specs.weight AS weight NUMERIC SORTABLE $.inventory[*].storecode AS store TAG $.inventory[*].instock AS instock NUMERIC SORTABLE
```

Example bike query...

```
127.0.0.1:6379> ft.search idx:bikes "@store:{CH} @material:{aluminium} @weight:[5 10] @instock:[3 5]" RETURN 5 stockcode brand model weight instock LIMIT 0 3 SORTBY instock DESC
1) (integer) 13
2) "redisbikeco:bike:rbc00083"
3)  1) "instock"
    2) "12"
    3) "stockcode"
    4) "RBC00083"
    5) "brand"
    6) "Peaknetic"
    7) "model"
    8) "Vesta"
    9) "weight"
   10) "8.2"
4) "redisbikeco:bike:rbc00030"
5)  1) "instock"
    2) "12"
    3) "stockcode"
    4) "RBC00030"
    5) "brand"
    6) "Bold bicycles"
    7) "model"
    8) "Mimas"
    9) "weight"
   10) "8.7"
6) "redisbikeco:bike:rbc00069"
7)  1) "instock"
    2) "5"
    3) "stockcode"
    4) "RBC00069"
    5) "brand"
    6) "Peaknetic"
    7) "model"
    8) "Hiiaka"
    9) "weight"
   10) "9.2"
```

Example store query:

```
TODO something with GEO
```

Start the application:

```
poetry run flask run
```

Then go to `http://localhost:5000`.