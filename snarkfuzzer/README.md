<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Before installation:
```sh
sudo apt-get update
```

General Dependencies
 * python3 (3.7 or higher required, helpful link for installing python3.10: https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux)
 * git 
 * valgrind
 ```sh
 sudo apt install python3 git valgrind
 ```
 * pip
 ```sh
 curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
 python3 get-pip.py
 ```

Python Dependencies
 * z3-solver
 * numpy
 * scipy
 * atheris (Clang required, installation guide can be found here: https://clang.llvm.org/get_started.html)
 * py_ecc
 ```sh
 sudo python3 -m pip install z3-solver numpy scipy py_ecc
 ```

Dependencies for py_ecc (use pip3 install)
 * mypy-extensions
 * eth_typing
 * eth_utils (Cython required)
 ```sh
 sudo python3 -m pip install mypy-extensions eth_typing Cython eth_utils
 ```

### Dependencies for some libraries
Dependencies for libsnark
 * build-essential
 * cmake (3.13.4 or higher)
 * libgmp3-dev
 * libprocps-dev
 * python3-markdown
 * libboost-program-options-dev
 * libssl-dev
 * pkg-config
 ```sh
 sudo apt install build-essential cmake git libgmp3-dev libprocps-dev python3-markdown libboost-program-options-dev libssl-dev pkg-config
 ```

 Dependencies for rust based libraries
 * cargo (installation guide can be found here: https://itsfoss.com/install-rust-cargo-ubuntu-linux/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/fanym919/snarktool.git
   ```
2. (Optional) Install Libsnark example program
   ```sh
   cd model/depends/
   python3 install.py
   ```
3. (Optional) Install Bellman example program
   ```sh
   cd model/depends/
   git clone https://github.com/arcalinea/bellman-examples.git
   cd bellman-examples
   cargo build
   ```

WARNING: Install target library in the depends directory. Please DO NOT use any optimization flag (such as O0, O1, O2) when compile the library. Optimization flag may damage the ability of the tool.

<!-- USAGE EXAMPLES -->
## Usage
1. Modify config.txt based on target library

2. Navigate to model/, run 
    ```python3 main.py
    ```
See main.py and config.txt for example usage.

## Demonstration
We provide a sample configuration file to demonstrate the ability of our tool. In this example, we test the security of libsnark Pinocchio protocol with py_ecc.

To run the demonstration, install all general, py_ecc, and libsnark dependencies. Then, install libsnark-tutorial (https://github.com/howardwu/libsnark-tutorial) in depends directory (see step 2 in Installation).

<!---
 README.md

| Library  | Language | Elliptic Curve | Protocol        |
| -------- | -------- | -------------- | --------------- |
| Libsnark | C++      | BN128          | PGHR13, Groth16 |
| Bellmen  | Rust     | BLS12-381      | Groth16         |

| Library | Language | Elliptic Curve   | EC Coordinate      |
| ------- | -------- | ---------------- | ------------------ |
| py_ecc  | Python   | BN128, BLS12-381 | Affine             |
| CIRCL   | Go       | BLS12-381        | Affine, Projective |


Depend Packages
1. general
	$ sudo apt install python3
	$ sudo apt install git
	$ sudo apt install python3-pip
	$ sudo apt install valgrind

2. python
	$ pip3 install z3-solver
	$ pip3 install numpy
	$ pip3 install scipy
	$ pip3 install atheris

	# for py_ecc only
	$ pip3 install mypy-extensions
	$ pip3 install eth_typing
	$ pip3 install eth_utils

3. libsnark
	$ sudo apt install build-essential cmake git libgmp3-dev libprocps-dev python3-markdown libboost-program-options-dev libssl-dev python3 pkg-config

4. bellman
    ...

5. golang
	# Download from https://go.dev/doc/install
	$ sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.18.3.linux-amd64.tar.gz
	# Add to .bashrc: export PATH=$PATH:/usr/local/go/bin

6. Rust
	$ sudo apt install curl
	$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
-->