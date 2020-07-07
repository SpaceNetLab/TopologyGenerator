# TopologyGenerator
A generator for constructing dynamic network topology. This generator can support routing or transport research on network topology with high mobility, such as satellite networks.

# Usage (this project is still under heavy development)

Assume you have already installed the docker environment(please check [Get Docker](https://docs.docker.com/get-docker/ ) and Python.

To run the emulation of constellation, fist run the `build_script.py` in `DockerMultiContainer` folder to generate the bash files.

```bash
python build_script.py
```
Then `build_emulator.sh` and `clean_emulator.sh` will be generated. 

Modify the orbit number and satellite number per orbit for your constellation. Please set a small value if your hardware capability is constrained.

```bash
#!/bin/bash
#build the constellation of starlink, where 1584 satellites into 72 orbital planes of 22 satellites each
ORBIT_NUM=72
SATELLITE_PER_ORBIT=22
```

Run the generation command.

```bash
./build_emulator.sh
```

Done. Contaioners will be created for emulation.

## Clean up
Clean all containers.
```bash
./clean_emulator.sh
```

Done.

