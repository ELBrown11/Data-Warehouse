#Purpose of this Database
Sparkify has grown their business and therefore increase their user base and song database. 
They  would like to move their data to the cloud to accommodate their need for more space.
Currently their data is stored in S3 in a directory of JSON logs, but they would like to 
move to a Redshift cloud database. As a data engineer my job is to creal ETL/ELT pipelines which 
would...
 * extract data from S3 -> stage in Redshift -> transform data into dimension table which 
can be used for analytics

#Justification of Database Schema Design and ETL pipeline
[Imgur](https://i.imgur.com/Y2fKlEi.png) <- this an ERD graphic for my database schema
* Database Schema Design
    * data is in a star schema which is optimal for queries on `song_plays`
* ETL pipeline
    * stages two tables (`events` and `songs`) from the two datasets previously stored in S3 
    * the staging of the two tables allows for creation of the fact and dimension tables which 
    make up the Redshift database
        * **fact table:** `song_plays`
        * **dimension tables:** `users`, `songs`, `artists`, `time`
##Files in Repository
* `sql_queries.py`
    * this file contains SQL statements which creates tables, drops tables, 
    stages tables in Redshift, copy tables to Redshift, and inserts data into the tables.
    These statements are imported into the other python files to be used in their functions 
    which enable the ETL pipeline. 
* `etl.py`
    * this file imports the copy table and insert table queries from `sql_queries.py`
    and uses them in it's functions to load data from S3 into staging tables on Redshift and process data 
    in analytics tables on Redshift
* `create_tables.py`
    * this file imports the create table and drop table queries from `sql_queries.py` 
    and uses them in it's functions to removes any previous table of the same names and then 
    create new fact and dimension tables in star schema in Redshift.
* `dwh.cfg`
    * this file contains Redshift database and IAM role info
 
##How To Run Files
1. Run `create_tables.py` which imports SQL from `sql_queries.py` to create tables and 
connect to the database so that data can be inserted into them later.
2. Run `etl.py` after running `create_tables.py` so load data from S3 to staging tables
on Redshift then load data from staging tables to analytics tables on Redshift.
    * for this step you do need to launch a Redshift cluster and create an IAM role
    with access to S3 
        * [See this link for help!](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-launch-sample-cluster.html)
3. To test your database run an analytics query and analyze your results 

    






