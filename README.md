# gerritaction

[![Actions Status](https://github.com/craftslab/gerritaction/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/craftslab/gerritaction/actions?query=workflow%3ACI)
[![License](https://img.shields.io/github/license/craftslab/gerritaction.svg?color=brightgreen)](https://github.com/craftslab/gerritaction/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/gerritaction.svg?color=brightgreen)](https://pypi.org/project/gerritaction)
[![Tag](https://img.shields.io/github/tag/craftslab/gerritaction.svg?color=brightgreen)](https://github.com/craftslab/gerritaction/tags)



## Introduction

*gerritaction* is a tool used for Gerrit action via Gerrit API.



## Prerequisites

- Python >= 3.7.0



## Run

```bash
git clone https://github.com/craftslab/gerritaction.git

cd gerritaction
pip install -Ur requirements.txt
python action.py --config-file="config.yml" --change-query="since:2024-01-01 until:2024-01-02"
```



## Docker

```bash
git clone https://github.com/craftslab/gerritaction.git

cd gerritaction
docker build --no-cache -f Dockerfile -t craftslab/gerritaction:latest .
docker run -it -v /tmp:/tmp craftslab/gerritaction:latest ./gerritaction --config-file="config.yml" --change-query="since:2024-01-01 until:2024-01-02"
```



## Usage

```
usage: action.py [-h] --config-file CONFIG_FILE
                 [--account-query ACCOUNT_QUERY] [--change-query CHANGE_QUERY]
                 [--change-action CHANGE_ACTION] [--group-query GROUP_QUERY]
                 [--project-query PROJECT_QUERY] [--output-file OUTPUT_FILE]
                 [-v]

Gerrit Action

options:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        config file (.yml)
  --account-query ACCOUNT_QUERY
                        account query (name:john email:example.com)
  --change-query CHANGE_QUERY
                        change query (status:open since:2024-01-01
                        until:2024-01-02)
  --change-action CHANGE_ACTION
                        change action (add-reviewer:account-id,... delete-
                        reviewer:account-id,... add-attention:account-id,...
                        remove-attention:account-id,... approve-change:Code-
                        Review=+2,... delete-change submit-change)
  --group-query GROUP_QUERY
                        group query (name:admin member:john)
  --project-query PROJECT_QUERY
                        project query (name:test state:active)
  --output-file OUTPUT_FILE
                        output file (.json)
  -v, --version         show program's version number and exit
```



## Settings

*gerritaction* parameters can be set in the directory [config](https://github.com/craftslab/gerritaction/blob/master/gerritaction/config).

An example of configuration in [config.yml](https://github.com/craftslab/gerritaction/blob/master/gerritaction/config/config.yml):

```yaml
apiVersion: v1
kind: worker
metadata:
  name: gerritaction
spec:
  gerrit:
    host: http://127.0.0.1/
    port: 8080
    user: user
    pass: pass
```



## License

Project License can be found [here](LICENSE).
