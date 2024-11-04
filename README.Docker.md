### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:80.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)

## API Reference
 
- Curl commando to test:
    - curl -X POST http://192.168.1.95:5000/api/translate -H "Content-Type: application/json" -d '{"url": "https://madsblog.net/2024/10/29/kubernetes-networking-parte-2/", "translator_api": "azure", "azure_endpoint": "https://api.cognitive.microsofttranslator.com/", "azure_credentials": "bccaadcc92794b6994ae0baa9ba90b9b"}'