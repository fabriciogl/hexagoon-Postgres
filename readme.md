## 1

-> GIT Clone https://github.com/fabriciogl/hexagoon.git

## 2

--> Having python 3.10 installed, use ``` pip install poetry ```

## 3

--> Inside the root app folder run ``` poetry install ```

## 4

--> create a ```.secrets.toml``` file with the following content inside the root folder, replacing the password for each enviroment:

<code> 
[default] <br>
root_senha = "cookies" <br>
db_pass = "secret" <br>
hash_1 = "3aabce021b58ee1f052484dc6787de8556d308b8" <br>
hash_2 = "HS256" <br>
[production] <br> 
root_senha = "cookies" <br>
db_pass = "secret"<br>
hash_1 = "3aabce021b58ee<br>1f052484dc6787de8556d308b8" <br>
hash_2 = "HS256" <br>
[development] <br>
root_senha = "cookies" <br>
db_pass = "secret" <br>
hash_1 = "3aabce021b58ee1f052484dc6787de8556d308b8" <br>
hash_2 = "HS256" <br>
[testing] <br>
root_senha = "cookies" <br>
db_pass = "secret" <br>
hash_1 = "3aabce021b58ee1f052484dc6787de8556d308b8" <br>
hash_2 = "HS256" 
</code>


## 5 

--> install postgres with docker

``` docker pull postgres:13```

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