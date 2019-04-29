# Automated grocery shopping with Nemlig.com

This pet project aims to automate the process of shopping groceries in [Nemlig.com](https://www.nemlig.com/), by imitation your previous shopping patterns. To fill your next basket, you just type:

    pipenv run python robot/main.py

Dig into the source code if you want to learn more about the algorithm(s) used for next basket prediction in this project.

## Nemlig.com API client (unofficial)

To list previous orders, add products to basket, etc. the robot uses a non-advertised REST API discovered by inspecting network traffic while using the Nemlig.com website.

The `api` directory in this repo provides a thin API client based on [Requests](https://2.python-requests.org/en/master/). It is built for the shopping robot, but could be used in other Nemlig.com automation projects as well.

## Let me know if you find this useful

I might just be the only person lazy enough to need automated grocery shopping. If this is *not* the case, and you actually give this robot a try, I would love to hear from you.

Open an [issue](https://github.com/schourode/nemlig/issues) if you have feedback or :star: the repo just to let me know that you are out there!
