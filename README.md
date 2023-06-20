# Redis Bike Company Example Application

TODO README!

```
poetry install
```

Create an environment file:

```
cp env.example .env
```

```
poetry run python data_loader.py
```

INDEX CREATION COMMANDS:

Stores index:

```
FT.CREATE idx:stores ON JSON PREFIX 1 redisbikeco:store: SCHEMA $.storecode AS storecode TAG $.storename AS storename TAG $.address.city AS city TAG $.address.state AS state TAG $.address.pin AS pin TAG $.address.country AS country TAG $.position AS position GEO $.amenities AS amenities TAG
```

Bikes index:

```
FT.CREATE idx:bikes ON JSON PREFIX 1 redisbikeco:bike: SCHEMA $.stockcode AS stockcode TAG SORTABLE $.model AS model TAG SORTABLE $.brand AS brand TAG SORTABLE $.type as type TAG SORTABLE $.description AS description TEXT $.specs.material AS material TAG SORTABLE $.specs.weight AS weight NUMERIC SORTABLE $.price AS price NUMERIC SORTABLE
```

Which aluminium bikes weigh between 5 and 10kg?:

```
127.0.0.1:6379> ft.search idx:bikes "@material:{aluminium} @weight:[5 10]" RETURN 4 stockcode brand model weight LIMIT 0 3 SORTBY weight ASC
1) (integer) 19
2) "redisbikeco:bike:rbc00074"
3) 1) "weight"
   2) "7.3"
   3) "stockcode"
   4) "RBC00074"
   5) "brand"
   6) "BikeShind"
   7) "model"
   8) "Iapetus"
4) "redisbikeco:bike:rbc00057"
5) 1) "weight"
   2) "7.5"
   3) "stockcode"
   4) "RBC00057"
   5) "brand"
   6) "nHill"
   7) "model"
   8) "Nereid"
6) "redisbikeco:bike:rbc00009"
7) 1) "weight"
   2) "7.9"
   3) "stockcode"
   4) "RBC00009"
   5) "brand"
   6) "nHill"
   7) "model"
   8) "Quaoar"
```

Which kids bikes cost less than 10,000 Rupees?

```
127.0.0.1:6379> ft.search idx:bikes "@type:{Kids Bikes} @price:[-inf 9999]" return 3 brand model price
1) (integer) 3
2) "redisbikeco:bike:rbc00058"
3) 1) "brand"
   2) "Peaknetic"
   3) "model"
   4) "Quaoar"
   5) "price"
   6) "7764"
4) "redisbikeco:bike:rbc00093"
5) 1) "brand"
   2) "Peaknetic"
   3) "model"
   4) "Titan"
   5) "price"
   6) "8359"
6) "redisbikeco:bike:rbc00098"
7) 1) "brand"
   2) "Tots"
   3) "model"
   4) "Ganymede"
   5) "price"
   6) "9439"
```

What different types of bike are there?

```
127.0.0.1:6379> ft.aggregate idx:bikes "*" groupby 1 @type
1) (integer) 7
2) 1) "type"
   2) "Enduro Bikes"
3) 1) "type"
   2) "Kids Bikes"
4) 1) "type"
   2) "Road Bikes"
5) 1) "type"
   2) "Mountain Bikes"
6) 1) "type"
   2) "Commuter Bikes"
7) 1) "type"
   2) "Kids Mountain Bikes"
8) 1) "type"
   2) "eBikes"
```

Which road bikes are either carbon or full-carbon?

```
127.0.0.1:6379> ft.search idx:bikes "@type:{Road Bikes} @material:{carbon|full\\-carbon}"
 1) (integer) 7
 2) "redisbikeco:bike:rbc00008"
 3) 1) "$"
    2) "{\"stockcode\":\"RBC00008\",\"model\":\"Polydeuces\",\"brand\":\"7th Generation\",\"price\":52350,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"full-carbon\",\"weight\":11.4},\"description\":\"Sharing features of more expensive bikes, this bike has a compact frame with a sloping top tube, D-Fuse seatpost and carbon fork. That gives great comfort and handling, letting you ride for longer and inspiring confidence. The Shimano gear system effectively does away with an external cassette, so is super low maintenance in terms of wear and tear. It's for the rider who wants both efficiency and capability.\"}"
 4) "redisbikeco:bike:rbc00050"
 5) 1) "$"
    2) "{\"stockcode\":\"RBC00050\",\"model\":\"Titania\",\"brand\":\"Bicyk\",\"price\":226645,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"carbon\",\"weight\":16.2},\"description\":\"The bike has a lightweight form factor, making it easier for seniors to use. At this price point, you get a Shimano 105 hydraulic groupset with a RS510 crank set. The wheels have had a slight upgrade for 2022, so you're now getting DT Swiss R470 rims with the Formula hubs. It comes fully assembled (no convoluted instructions!) and includes a sturdy helmet at no cost.\"}"
 6) "redisbikeco:bike:rbc00072"
 7) 1) "$"
    2) "{\"stockcode\":\"RBC00072\",\"model\":\"Ariel\",\"brand\":\"Velorim\",\"price\":172833,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"carbon\",\"weight\":10.9},\"description\":\"The bike has a lightweight form factor, making it easier for seniors to use. The hydraulic disc brakes provide powerful and modulated braking even in wet conditions, whilst the 3x8 drivetrain offers a huge choice of gears. It's for the rider who wants both efficiency and capability.\"}"
 8) "redisbikeco:bike:rbc00028"
 9) 1) "$"
    2) "{\"stockcode\":\"RBC00028\",\"model\":\"Enterprise\",\"brand\":\"Bold bicycles\",\"price\":227103,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"full-carbon\",\"weight\":13.0},\"description\":\"This is our entry-level road bike for 2023 but it not a basic machine. The Plush saddle softens over time with use. The included Seatpost, however, is easily adjustable and adds to this bike's fantastic rating, as do the hydraulic disc brakes from Tektro. Put it all together and you get a bike that helps redefine what can be done for this price.\"}"
10) "redisbikeco:bike:rbc00059"
11) 1) "$"
    2) "{\"stockcode\":\"RBC00059\",\"model\":\"Vanth\",\"brand\":\"Ergonom\",\"price\":178352,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"carbon\",\"weight\":13.5},\"description\":\"Sharing features of more expensive bikes, this bike has a compact frame with a sloping top tube, D-Fuse seatpost and carbon fork. That gives great comfort and handling, letting you ride for longer and inspiring confidence. The Plush saddle softens over time with use. The included Seatpost, however, is easily adjustable and adds to this bike's fantastic rating, as do the hydraulic disc brakes from Tektro. Put it all together and you get a bike that helps redefine what can be done for this price.\"}"
12) "redisbikeco:bike:rbc00088"
13) 1) "$"
    2) "{\"stockcode\":\"RBC00088\",\"model\":\"Polydeuces\",\"brand\":\"Tots\",\"price\":190856,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"full-carbon\",\"weight\":8.2},\"description\":\"This bike delivers a lot of bike for the money. It has a lightweight frame and all-carbon fork, with cables routed internally. Put it all together and you get a bike that helps redefine what can be done for this price.\"}"
14) "redisbikeco:bike:rbc00015"
15) 1) "$"
    2) "{\"stockcode\":\"RBC00015\",\"model\":\"Hygiea\",\"brand\":\"Bicyk\",\"price\":201355,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"full-carbon\",\"weight\":7.0},\"description\":\"This bike delivers a lot of bike for the money. The hydraulic disc brakes provide powerful and modulated braking even in wet conditions, whilst the 3x8 drivetrain offers a huge choice of gears. That said, we feel this bike is a fantastic option for the rider seeking the versatility that this highly adjustable bike provides.\"}"
```

Which bikes are comfortable, but not made of aluminium or alloy?

```
127.0.0.1:6379> ft.search idx:bikes "@description:comfortable -@material:{aluminium|alloy}"
1) (integer) 2
2) "redisbikeco:bike:rbc00008"
3) 1) "$"
   2) "{\"stockcode\":\"RBC00008\",\"model\":\"Polydeuces\",\"brand\":\"7th Generation\",\"price\":52350,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"full-carbon\",\"weight\":11.4},\"description\":\"Sharing features of more expensive bikes, this bike has a compact frame with a sloping top tube, D-Fuse seatpost and carbon fork. That gives great comfort and handling, letting you ride for longer and inspiring confidence. The Shimano gear system effectively does away with an external cassette, so is super low maintenance in terms of wear and tear. It's for the rider who wants both efficiency and capability.\"}"
4) "redisbikeco:bike:rbc00059"
5) 1) "$"
   2) "{\"stockcode\":\"RBC00059\",\"model\":\"Vanth\",\"brand\":\"Ergonom\",\"price\":178352,\"type\":\"Road Bikes\",\"specs\":{\"material\":\"carbon\",\"weight\":13.5},\"description\":\"Sharing features of more expensive bikes, this bike has a compact frame with a sloping top tube, D-Fuse seatpost and carbon fork. That gives great comfort and handling, letting you ride for longer and inspiring confidence. The Plush saddle softens over time with use. The included Seatpost, however, is easily adjustable and adds to this bike's fantastic rating, as do the hydraulic disc brakes from Tektro. Put it all together and you get a bike that helps redefine what can be done for this price.\"}"
```

Modifying JSON documents to add a thumbs up count (to several bikes):

```
127.0.0.1:6379> json.mset redisbikeco:bike:rbc00013 $.thumbsup 2 redisbikeco:bike:rbc00034 $.thumbsup 3 redisbikeco:bike:rbc00099 $.thumbsup 1
OK
```

Update the bikes index to add the thumbs up data:

```
127.0.0.1:6379> ft.alter idx:bikes schema add $.thumbsup as thumbsup numeric sortable
OK
```

Query the new field:

```
127.0.0.1:6379> ft.search idx:bikes "@thumbsup:[0 +inf]" return 3 brand model thumbsup sortby thumbsup desc
1) (integer) 3
2) "redisbikeco:bike:rbc00034"
3) 1) "thumbsup"
   2) "3"
   3) "brand"
   4) "7th Generation"
   5) "model"
   6) "Callisto"
4) "redisbikeco:bike:rbc00013"
5) 1) "thumbsup"
   2) "2"
   3) "brand"
   4) "Bold bicycles"
   5) "model"
   6) "Ariel"
6) "redisbikeco:bike:rbc00099"
7) 1) "thumbsup"
   2) "1"
   3) "brand"
   4) "ScramBikes"
   5) "model"
   6) "Proteus"
```

Which stores provide parking and rent bikes to customers?

```
127.0.0.1:6379> ft.search idx:stores "@amenities:{parking} @amenities:{rentals}"

1) (integer) 2
2) "redisbikeco:store:ch"
3) 1) "$"
   2) "{\"storecode\":\"CH\",\"storename\":\"Chennai\",\"address\":{\"street\":\"Arcot Road\",\"city\":\"Chennai\",\"state\":\"Tamil Nadu\",\"pin\":\"600026\",\"country\":\"India\"},\"position\":\"80.2057207,13.0511065\",\"amenities\":[\"parking\",\"rentals\",\"repairs\"]}"
4) "redisbikeco:store:ko"
5) 1) "$"
   2) "{\"storecode\":\"KO\",\"storename\":\"Kochi\",\"address\":{\"street\":\"Mulamkuzhi Beach Road\",\"city\":\"Kochi\",\"state\":\"Kerala\",\"pin\":\"682002\",\"country\":\"India\"},\"position\":\"76.2415241,9.9436983\",\"amenities\":[\"parking\",\"rentals\",\"repairs\",\"wifi\"]}"
```

Modify JSON documents to change some store amenities:

```
127.0.0.1:6379> json.arrappend redisbikeco:store:be $.amenities '"parking"'
1) (integer) 5
127.0.0.1:6379> json.arrindex redisbikeco:store:ch $.amenities '"rentals"'
1) (integer) 1
127.0.0.1:6379> json.arrpop redisbikeco:store:ch $.amenities 1
1) "\"rentals\""
127.0.0.1:6379> json.get redisbikeco:store:ch $.amenities
"[[\"parking\",\"repairs\"]]"
```

Query store amenities again to verify that the index was updated automatically:

```
127.0.0.1:6379> ft.search idx:stores "@amenities:{parking} @amenities:{rentals}" return 1 storename
1) (integer) 2
2) "redisbikeco:store:ko"
3) 1) "storename"
   2) "Kochi"
4) "redisbikeco:store:be"
5) 1) "storename"
   2) "Bengaluru"
```

Add further address information for a store:

```
127.0.0.1:6379> json.merge redisbikeco:store:ko $.address '{"what3words": "yellow train cloud", "number": "12"}'
OK
127.0.0.1:6379> json.get redisbikeco:store:ko $
"[{\"storecode\":\"KO\",\"storename\":\"Kochi\",\"address\":{\"street\":\"Mulamkuzhi Beach Road\",\"city\":\"Kochi\",\"state\":\"Kerala\",\"pin\":\"682002\",\"country\":\"India\",\"what3words\":\"yellow train cloud\",\"number\":\"12\"},\"position\":\"76.2415241,9.9436983\",\"amenities\":[\"parking\",\"rentals\",\"repairs\",\"wifi\"]}]"
```

Which stores are within 100km of Lucknow?

```
127.0.0.1:6379> ft.search idx:stores "@position:[80.8599399 26.848668 100 km]" return 2 storecode city
1) (integer) 1
2) "redisbikeco:store:ka"
3) 1) "storecode"
   2) "KA"
   3) "city"
   4) "Kanpur"
```

Start the application:

```
poetry run flask run
```

Then go to `http://localhost:5000`.