# locust boshrelease

A boshrelease to deploy [locus](https://locust.io/) in master/slaves mode.

## Deploy

1. Clone this repo
2. Run `bosh -d locust deploy manifests/main.yml`

You can add more specific configuration by using operations file accessible here: [/manifest/operations](/manifest/operations)

## Add more slave

Use ops file [/manifest/operations/add-slaves.yml](/manifest/operations/add-slaves.yml) during deployment 
and set var `locust_slaves` to defined how many slaves you want:

```bash
bosh -d locust deploy manifests/main.yml -o manifests/operations/add-slaves.yml -v locust_slaves=6
```