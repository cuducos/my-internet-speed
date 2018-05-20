[![Tests](https://img.shields.io/travis/cuducos/my-internet-speed.svg)](https://travis-ci.org/cuducos/my-internet-speed)
[![Coverage](https://img.shields.io/codeclimate/coverage/cuducos/my-internet-speed.svg)](https://codeclimate.com/github/cuducos/my-internet-speed)
[![Maintainability](https://img.shields.io/codeclimate/maintainability-percentage/cuducos/my-internet-speed.svg)](https://codeclimate.com/github/cuducos/my-internet-speed)

# My Internet Speed

I wrote this app so I can **periodically** monitor my internet speed and:

* Collect data to build a report about the quality of the service provided by
  my ISP
* Automatically tweet my ISP when the speed is lower than expected – surely
  **optional**
* Store speed test results in PostgreSQL
* Check all speed test results in a web API
* Monitor all speed test tasks

At home this runs on my Raspberry Pi.

## Installing

### Requirements

**It is important** to run this app in a computer connected to the internet via
ethernet cable, **not via wireless** – this is the way to have a good accuracy
in testing the speed.

* [Docker](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

Optionally, if you want the Twitter feature to work (it will **only** tweet
when the speed is below the configures threshold):

* Twitter consumer key and secret
* Twitter access token and access token secret

You can get these Twitter credentials at the [Twitter Application Management
dashboard](https://apps.twitter.com/).

### Settings

Before you get started, copy `.env.sample` as `.env` and edit as follows:

1. Set `INTERVAL` according to how often (in minutes) you want to run the speed
   test (e.g.: `20` for _20min_)
1. Set your `TIMEZONE` accordingly

If you want the app to post tweets:

1. Add your Twitter credentials at the top of the file
1. Set `CONTRACT_SPEED` to the speed in Mbps you are paying for (e.g.: `60` if
   you contract says _60Mbps_)
1. Set `THRESHOLD` to the minimum percentage of the contract speed you contract
   or local laws enforces your ISP (e.g.: `0.4` for 40%)
1. Set your tweet message using `{contract_speed}` where the contract speed in
   Mbps should be (for example, `60` for _60Mbps_), `{real_speed}` where the
   measured speed should be, and `{percentage}` where comparing both should be
   (feel free to use the Twitter handle of your ISP too)
1. Add `{result_url}` in order to add the link to the result provided by
   [SpeedTest](https://speedtest.net)

For example, if:

* the measured speed is 20Mpbs
* your `CONTRACT_SPEED` is `60`
* the `THRESHOLD` is `0.4`
* and `TWEET` is configures as  `I pay for {contract_speed}, but now @MyISP is
  working at {real_speed} – merely {percentage} of what I'm paying for :(
  {result_url}`

The final tweet would be:

> I pay for 60Mbps, but now @MyISP is working at 20Mbps – merely 33% of what
> I'm paing for :( http://www.speedtest.net/result/7307126311

If you like this app, add `#MyInternetSpeed
https://github.com/cuducos/my-internet-speed` to your tweets ; )

### Database

This `docker-compose.yml` lefts out the `db` container from all possible
`depends_on` in order to make it easier to use an external/remote database to
persist data (just point `POSTGRES`s variables and the `PGRST` ones to
somewhere else).

Thus if you are using the Docker database it is useful to start it manually
first:

```console
$ docker-compose up -d db
```

In both cases run this one off command to create the database tables:

```console
$ docker-compose run --rm beat python \
  -c "from my_internet_speed.models import Result; Result.create_table()"
```

### Spinning up the app

```console
$ docker-compose up -d
```

This spins up the periodic tasks as well as two other services so you can
monitor:

* [All speed test results](https://localhost:3000)
* [All speed test tasks](https://localhost:5555)

#### Troubleshooting

##### `UnixHTTPConnectionPool(host='localhost', port=None): Read timed out.`

I was getting this error in my Raspberry Pi when trying to run `docker-compose
up`. This seams to be a workaround:

```console
$ export DOCKER_CLIENT_TIMEOUT=600
$ export COMPOSE_HTTP_TIMEOUT=600
```