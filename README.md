# Network Automation

## Example 2: Github actions
This is a test of github actions.
starting with a simple example:

Create file ".github/workflows/demo-workflow-file.yml" with the following content:
 
```
on: [push]

jobs:
  build:
    name: Hello world
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Write a multi-line message
      run: |
        echo This demo file shows a 
        echo very basic and easy-to-understand workflow.
```

The actions will be triggered on push.


## Example 2: Drone

Install Drone and a runner. Create ./drone.yml file

```
kind: pipeline
type: docker
name: Testing Python CI/CD


steps:
- name: Install and deploy
  image: python
  commands:
  - pip3 install -r requirements.txt
  - python3 bat.py

trigger:
  branch:
    exclude:
    - main
    - master
```

