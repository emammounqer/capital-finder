# Class 16 - Capital Finder

## Routes

### GET /api/capital-finder

Query params:

- Country: name of the country
- Capital: name of the capital

### Examples

`https://capital-finder-jordan-first.vercel.app/api/capital-finder?country=spain&capital=madrid`

Response:

```txt
Yes, madrid is the capital of spain,
its currency is EUR, and the population is 47351567, the Language is Spanish, 
```

`https://capital-finder-jordan-first.vercel.app/api/capital-finder?country=jordan`

Response:

```txt
Capital of jordan is Amman
its currency is JOD, and the population is 10203140, the Language is Arabic, 
```

`https://capital-finder-jordan-first.vercel.app/api/capital-finder?capital=amman`

Response:

```txt
amman is the capital of Jordan
its currency is JOD, and the population is 10203140, the Language is Arabic, 
```
