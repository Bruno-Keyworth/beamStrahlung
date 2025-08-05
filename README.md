# Very Brief How-To-Use

## 1. Create the environment variable `codeDir`

Set the `codeDir` environment variable such that it points to the path of the parent directory containing the `k4geo` and `beamStrahlung` repositories. These two repositories should be located in the same parent directory.

## 2. Set up the machine identifier

This code base is designed to run on different machines with various software configurations for interacting with high-throughput computing clusters (currently supporting `HTCondor` and `IBM Spectrum LSF`) and different directory structures. The system identifies the machine based on the user name.

You need to create a file named `uname_to_sys_map.json`, where the key is your user name and the value is a so-called `MACHINE_IDENTIFIER`. Below are examples for the fictitious user A. Einstein:

- ### For DESY NAF (user name: `einsteina`)

  ```json
  {
    "einsteina": "desy-naf"
  }
  ```

- ### For KEK (user name: `einstein`)

  ```json
  {
    "einstein": "kek"
  }
  ```

- ### For both systems (if you need both mappings)

  ```json
  {
    "einsteina": "desy-naf",
    "einstein": "kek"
  }
  ```

- For more information, check out the `platform_paths.py` file.

- ### Important Notes on Cluster Interfaces

  - The **HTCondor** interface has been actively used and tested in recent developments.
  - The **IBM Spectrum LSF** interface (used at KEK) has not been tested recently and may require additional adjustments.

## 3. Tip

You can always use the `--help` or `-h` flag to get more information about the available command-line arguments for the Python scripts:

```bash
python simall.py --help
```

## 4. Simulate particle propagation through the detector model(s) and its response

Run the following command to simulate the particle propagation:

```bash
python simall.py --version test --detectorModel ILD_l5_v02 ILD_FCCee_v01 --scenario FCC240 FCC091 ILC250
```

## 5. Evaluate generated data

To evaluate the generated data, run one of the following commands:

- If you have the `dtDir` environment variable set:

  ```bash
  python combined_analysis.py --version test --mode overview
  ```

- Otherwise, provide the data directory path explicitly:

  ```bash
  python combined_analysis.py --directory $HOME/promotion/data/test --mode overview
  ```

## 6. Perform the analysis

To perform the analysis, use:

```bash
python combined_analysis.py --version test --mode analysis
```
