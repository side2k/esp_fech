import argparse
from parsel import Selector
import requests

parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument(
    "--source",
    type=int,
    help="show only metrics from one source with this index")
parser.add_argument(
    "--source-names", action="store_true",
    help="show source names and indices")
parser.add_argument(
    "--param-names", action="store_true",
    help="show param names")
parser.add_argument(
    "--param",
    help="show only one param with specified name"
    "(you can use few first chars here, case insensitive)")
parser.add_argument(
    "--munin-title-only", action="store_true",
    help="output graph title for Munin")

args = parser.parse_args()

url = "http://{args.host}".format(args=args)

response = requests.get(url)
root = Selector(response.text)
data = {}

for header in root.xpath("//div[contains(@class, 'blockk')][1]/b"):
    name = header.xpath("text()").extract_first()
    name = name.strip().strip(":")

    values = []
    data[name] = values

    for node in header.xpath("following-sibling::node()"):
        [tag] = node.xpath("name()").extract() or [None]
        if tag == 'b':
            break

        if not tag:
            for value in node.re("((?:^| +)\w+\: +[\d\.]+)"):
                metric, val = [part.strip() for part in value.split(":")]
                values.append((metric, val))

names = sorted(data.keys())
for index, name in enumerate(names):
    if args.source is not None and index != args.source:
        continue
    if args.source_names:
        print "---source #{}: {}".format(index, name)
    for param_name, value in data[name]:
        if args.param and not param_name.lower().startswith(args.param.lower()):
            continue
        if args.munin_title_only:
            print "{} sensor {}: {}".format(args.host, name, param_name)
            break
        format_str = "{name}: {value}" if args.param_names else "{value}"
        print format_str.format(name=param_name, value=value)
