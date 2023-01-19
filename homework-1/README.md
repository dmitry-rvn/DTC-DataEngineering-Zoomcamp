# Week 1 Homework

### Question 1. Knowing docker tags

Which tag has the following text? - Write the image ID to the file
```commandline
docker build --help
```
Answer: **--iidfile string**

### Question 2. Understanding docker first run

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed ( use pip list). How many python packages/modules are installed?

Answer: **3**

------

#### Preparations for Q3-6:

```commandline
docker build -t taxi_ingest:v1 .
docker-compose up
docker run -it --network=dbnetwork taxi_ingest:v1 --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=green_taxi_trips --date_cols=lpep_pickup_datetime,lpep_dropoff_datetime --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
docker run -it --network=dbnetwork taxi_ingest:v1 --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=zones --url=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

### Question 3. Count records

```postgres-sql
/* 
How many taxi trips were totally made on January 15?
Tip: started and finished on 2019-01-15.
*/

SELECT COUNT(*)
FROM green_taxi_trips t
WHERE DATE_TRUNC('day', t.lpep_pickup_datetime) = '2019-01-15' 
AND DATE_TRUNC('day', t.lpep_dropoff_datetime) = '2019-01-15'
```
Answer: **20530**

### Question 4. Largest trip for each day

```postgres-sql
/* 
Which was the day with the largest trip distance?
Use the pick up time for your calculations.
*/

SELECT DATE_TRUNC('day', t.lpep_pickup_datetime) AS date, t.trip_distance
FROM green_taxi_trips t
ORDER BY t.trip_distance DESC
LIMIT 1
```
Answer: **2019-01-15**

### Question 5. The number of passengers

```postgres-sql
/* 
In 2019-01-01 how many trips had 2 and 3 passengers?
*/

SELECT passenger_count, COUNT(*)
FROM green_taxi_trips t
WHERE DATE_TRUNC('day', t.lpep_pickup_datetime) = '2019-01-01'
AND passenger_count IN (2, 3)
GROUP BY passenger_count
```
Answer: **2: 1282 ; 3: 254**

### Question 6. Largest tip

```postgres-sql
/* 
For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip? 
We want the name of the zone, not the id.
*/

SELECT zd."Zone", t.tip_amount
FROM green_taxi_trips t
JOIN zones zp ON zp."LocationID" = t."PULocationID" AND zp."Zone" = 'Astoria'
JOIN zones zd ON zd."LocationID" = t."DOLocationID"
ORDER BY t.tip_amount DESC
LIMIT 1
```
Answer: **Long Island City/Queens Plaza**
