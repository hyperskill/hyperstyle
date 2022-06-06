from lxml import etree

root = etree.fromstring(input())
children = root.getchildren(root)
