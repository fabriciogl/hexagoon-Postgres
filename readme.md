## 1 CLONE THE PROJECT

-> GIT Clone https://github.com/fabriciogl/hexagoon.git

## 2 POETRY

--> Having python 3.10 installed, use ``` pip install poetry ```

## 4 INSTALL PACKAGES

--> Inside the root app folder run ``` poetry install ```

## 4 SECRETS

--> create a ```.secrets.toml``` file with the following content inside the root folder, replacing the password for each enviroment:

--> replace the values with your own settings  
--> ``` [default] ``` is mandatory, even if you don't use as an environment.    
--> ``` [production] [development] [testing] ``` are used when necessary  

<code>
[default]<br/>  
root_pass = "cookies" <br/>  
db_pass = "secret" <br/>  
dns = "oracleService" <br/>  
jwt_hash = "longHash" <br/>  
jwt_algo = "HS256" <br/>  
root_user = "" <br/>  
root_email = "" <br/>  
root_role = "root" <br/>  
db_driver = "" <br/>  
db_user = "" <br/>  
db_address = "" <br/>  
[production] <br/>  
root_pass = "cookies" <br/>  
db_pass = "secret" <br/>  
dns = "oracleService"  <br/>  
jwt_hash = "longHash" <br/>  
jwt_algo = "HS256" <br/>  
root_user = "" <br/>  
root_email = "" <br/>  
root_role = "root" <br/>  
db_driver = "" <br/>  
db_user = "" <br/>  
db_address = "" <br/>  
[development] <br/>  
root_pass = "cookies" <br/>  
db_pass = "secret" <br/>  
dns = "oracleService"  <br/>  
jwt_hash = "longHash" <br/>  
jwt_algo = "HS256" <br/>  
root_user = "" <br/>  
root_email = "" <br/>  
root_role = "root" <br/>  
db_driver = "" <br/>  
db_user = "" <br/>  
db_address = "" <br/>  
[testing] <br/>  
root_pass = "cookies" <br/>  
db_pass = "secret" <br/>  
dns = "oracleService"  <br/>  
jwt_hash = "longHash" <br/>  
jwt_algo = "HS256" <br/>  
root_user = "" <br/>  
root_email = "" <br/>  
root_role = "root" <br/>  
db_driver = "" <br/>  
db_user = "" <br/>  
db_address = "" <br/>  
</code>


## 5 

--> install postgres with docker

``` docker pull postgres:latest```

## 6

--> configure postgres

``` docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=secret -d postgres```

## 7

--> Using Pycharm, create a server run/debug configuration and add following variables to env

    - ENV_FOR_DYNACONF=development;

## 8

--> run aplication on Pycharm

## 9 

--> stopping your app

stop pycharm run/debug server and ``` docker stop postgres ```

--> restarting your app

``` docker start postgres ``` and start pycharm run/debug server
