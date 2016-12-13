# esp_fech
Simple utility to fetch data from ESP8266-based module(see https://wifi-iot.com/)

## Usage

Most simple invocation: `python esp_fetch.py esp8266.host.or.ip`, for example:

```
python esp_fetch.py 192.168.0.113
```
It will just output all found data without the source and param names

Other command line arguments:

 * `--source-names` - show source names
 * `--param-names` - show param names
 * `--source <index>` - show data from only one source with index `index`
 * `--param <param> - show only params with name matching `param`. Its case insensitive and you can use only a few first letters. For example - `temp` will match `Temperature`

Full list of data can be obtained this way:

```
python esp_fetch.py 192.168.0.113 --source-names --param-names
```

it will output something like this:

```
---source #0: BMP085/180
Temperature: 30.1
Pressure: 748.56
---source #1: DHT11/22 1
Temperature: 14.5
Humidity: 29.8
---source #2: DHT11/22 2
Temperature: 37.5
Humidity: 13.1
```

Now apply some filtering:

```
$ python esp_fetch.py 192.168.0.113 --source 1 --param hum
29.8
```
