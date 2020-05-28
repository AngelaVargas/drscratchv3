drScratch
=========

drScratch is an analytical tool that evaluates your Scratch projects in a variety of computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelization, flow control, user interactivity and data representation. This analyzer is a helpful tool to evaluate your own projects, or those of your Scratch students.

You can try a beta version of drScratch at http://drscratch.org

### How to run drScratch server
```console
make build
make start
```

### How to activate translations
```console
make translate
```

### How to access to containers
```console
$ docker run -d -p 3306:3306 --name drscratchv3_database -e MYSQL_ROOT_PASSWORD=password mysql
$ docker exec -it drscratchv3_database mysql -p
$ docker exec -it drscratchv3_django bash
```