db_folder=. # This is the path on host (your computer) where the database will be stored
docker run -d --name aaa -p 3000:3000 -p 8000:8000 -v $db_folder:/db aaa
