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

[![Build Status](http://129.173.143.55/api/badges/martimy/Network-Automation/status.svg)](http://129.173.143.55/martimy/Network-Automation)
