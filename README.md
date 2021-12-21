# Zerohunger

Exploration tool for scholarly articles related to the [Zero Hunger](https://en.wikipedia.org/wiki/Sustainable_Development_Goals#Goal_2:_Zero_hunger) topic, part of the Sustainable Development Goals (SDGs) initiative.

This prototype was developed during the [SDGs Springer Nature hack day](http://www.michelepasin.org/blog/2019/02/11/zero-hunger-hack-day/).

More info: https://www.michelepasin.org/projects/zerohunger2018/index.html


## Tech info

This is a Django app which is mirrored in local using `wget` and rendered as a static site in /docs.

To experience all the app functionalities, it should be run using Django and a web server. 

The `docs` folder contains a static version of the site, which is accessible at: 

* http://zerohunger.michelepasin.org/


## Dimensions API credentials

Copy the local settings file first:

```bash
cp local_settings_example.py local_settings.py
```

Then update the [Dimensions API](https://docs.dimensions.ai/dsl) credentials as needed: 

```python
DIMENSIONS_USR = ""
DIMENSIONS_PSW = ""
```

## Status

This project is here for documentation purposes and is no longer under development.