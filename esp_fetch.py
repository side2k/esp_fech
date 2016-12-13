import argparse
from parsel import Selector
import requests

parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument(
    "--filter",
    type=int,
    help="show only metrics from one source with this index")
parser.add_argument(
    "--show-sources", action="store_true",
    help="show source names and indices")

args = parser.parse_args()
print args

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
    if args.filter is not None and index != args.filter:
        continue
    if args.show_sources:
        print "---source #{}: {}".format(index, name)
    for param_name, value in data[name]:
        print param_name, value
