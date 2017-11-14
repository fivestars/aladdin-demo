# Code Mounting 

You may want to mount a host directory into a container so that if code is updated on the host machine, the changes will be reflected in the container after a simple restart, instead of needing to rebuild the container image every time. 

Aladdin supports this with a `--with-mount` option, which is populated in Helm as `deploy.withMount` variable. We can then mount the volumes in the desired containers. 

In our example, we can mount everything in the `app` directory into the `aladdin-demo` container in [server/deploy.yaml](../helm/aladdin-demo/templates/server/deploy.yaml).
```yaml
        volumeMounts:
{{ if .Values.deploy.withMount }}
          - mountPath: /home
            name: {{ .Chart.Name }}-server
{{ end }} # /withMount

     . . .

      volumes:
{{ if .Values.deploy.withMount }}
        - name: {{ .Chart.Name }}-server
          hostPath:
            path: {{ .Values.deploy.mountPath }}/app
{{ end }} 
```
Notice that in [app/Dockerfile](../app/Dockerfile), we copy over the code in `app` with `COPY app /home`, so everything still works when code mounting is turned off. The mounting will actually overrwrite these files, so the mounted code is used when `--with-mount` is used.
