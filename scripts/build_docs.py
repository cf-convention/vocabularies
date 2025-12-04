# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "jinja2",
#     "lxml",
# ]
# ///

import shutil
from collections import defaultdict
from pathlib import Path

import click
from jinja2 import Template
from lxml import etree

vocabularies = (
    "area-type-table",
    "cf-standard-names",
    "standardized-region-list",
)

index_template = Template("""\
<html>

<head>
    <title>CF Vocabularies Lists</title>
</head>

<body>
    <h1>CF Vocabularies</h1>
    <h2>CF Standard Names</h2>
    <h3>Current</h3>
    <a href="cf-standard-names/current/index.html">HTML</a>
    <a download href="cf-standard-names/current/cf-standard-name-table.xml">XML</a>
    <a href="cf-standard-names/kwic/index.html">KWIC Index</a>
    <h3>Versions</h3>
    <h4>HTML</h4>
    {% for version in context["cf-standard-names"]|sort(reverse=True) -%}
    <a href="cf-standard-names/version/{{version}}/cf-standard-name-table.xml">{{version}}</a>
    {% endfor -%}
    <h4>XML</h4>
    {% for version in context["cf-standard-names"]|sort(reverse=True) -%}
    <a download href="cf-standard-names/version/{{version}}/cf-standard-name-table.xml">{{version}}</a>
    {% endfor -%}
    <h4>KWIC Index</h4>
    {% for version in context["cf-standard-names"]|sort(reverse=True) -%}
    <a href="cf-standard-names/kwic/index.html?tableURI=../version/{{version}}/cf-standard-name-table.xml">{{version}}</a>
    {% endfor -%}
    <h2>Area Type Table</h2>
    <h3>Current</h3>
    <a href="area-type-table/current/index.html">HTML</a>
    <a download href="area-type-table/current/area-type-table.xml">XML</a>
    <h3>Versions</h3>
    <h4>HTML</h4>
    {% for version in context["area-type-table"]|sort(reverse=True) -%}
    <a href="area-type-table/version/{{version}}/area-type-table.xml">{{version}}</a>
    {% endfor -%}
    <h4>XML</h4>
    {% for version in context["area-type-table"]|sort(reverse=True) -%}
    <a download href="area-type-table/version/{{version}}/area-type-table.xml">{{version}}</a>
    {% endfor -%}
    <h2>Standardized Region List</h2>
    <h3>Current</h3>
    <a href="standardized-region-list/current/index.html">HTML</a>
    <a download href="standardized-region-list/current/standardized-region-list.xml">XML</a>
    <h3>Versions</h3>
    <h4>HTML</h4>
    {% for version in context["standardized-region-list"]|sort(reverse=True) -%}
    <a href="standardized-region-list/version/{{version}}/standardized-region-list.xml">{{version}}</a>
    {% endfor -%}
    <h4>XML</h4>
    {% for version in context["standardized-region-list"]|sort(reverse=True) -%}
    <a download href="standardized-region-list/version/{{version}}/standardized-region-list.xml">{{version}}</a>
    {% endfor -%}
</body>
</html>
""")

build_uri_prefix = "https://cfconventions.org/vocabularies/"


@click.command()
@click.argument(
    "root",
    type=click.Path(
        exists=True, file_okay=False, readable=True, writable=True, path_type=Path,
    ),
)
def build(root: Path):
    src_dir = root / "docs"
    build_dir = root / "_build"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    for base, dirs, files in src_dir.walk():
        for file in files:
            src_file = base / file
            destination = build_dir / src_file.relative_to(src_dir)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, destination)

    vocab_versions = defaultdict(list)

    for vocab in vocabularies:
        vocab_dir = src_dir / vocab
        version_dir = vocab_dir / "version"
        current_dir = build_dir / vocab / "current"
        current_index = current_dir / "index.html"

        current_version = 0
        for dir in version_dir.glob("*"):
            if not dir.name.isdigit():
                continue

            version = int(dir.name)
            vocab_versions[vocab].append(version)
            current_version = max(version, current_version)

        current_version_dir = version_dir / str(current_version)
        shutil.copytree(current_version_dir, current_dir)

        current_xml = list(current_version_dir.glob("*.xml"))[0]
        xml = etree.parse(current_xml)
        stylesheet: str = xml.xpath("/processing-instruction('xml-stylesheet')")[
            0
        ].attrib["href"]
        stylesheet = stylesheet.removeprefix(build_uri_prefix)
        stylesheet_path = build_dir / stylesheet

        html = xml.xslt(etree.parse(stylesheet_path))
        current_index.write_bytes(html)

    root_index = build_dir / "index.html"
    root_index.write_text(index_template.render(context=vocab_versions))


if __name__ == "__main__":
    build()
