## Getting Started

### Prerequisites

Before installation:
```sh
sudo apt-get update
```

General Dependencies
 * python3 (3.7 or higher required, helpful link for installing python3.10: https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux)
 * git
 * pip
 ```sh
 curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
 python3 get-pip.py
 ```

Python Dependencies
 * z3-solver
 * numpy
 ```sh
 sudo python3 -m pip install z3-solver numpy
 ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/fanym919/snarktool.git
   ```

## Usage
1. Modify config.txt based on target library

2. Write a python script to indicate the statement equation by using the API provide by this tool

3. Run your script to check the correctness of statement and circuit.

## Demonstration
We provide a sample configuration file to demonstrate the ability of our tool and provide instructions about how to use our tool.

There are three demonstration in the test directory.

cube1.py: a cube statement with correct circuit (manually flattening)

cube2.py: a cube statement with incorrect circuit (manually flattening)

range.py: a range statement with libsnark gadget

To run these demonstration, Navigate to constraints/, run 
    ```python3 test/cube1.py
    ```