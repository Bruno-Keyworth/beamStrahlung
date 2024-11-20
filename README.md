# Very brief how-to-use

1. create env var `myCodeDir`
   its value needs to be the parent dir path of the k4geo and beamStrahlung repos (it is assumed that they are located in the same parent dir)

2. `simall.py`
   atm config is hard-coded :(

3. Evaluate generate data
   `python combined_analysis.py --directory $HOME/promotion/data/ecfa --mode overview`

   - in case of problems try: `python analyze_available_data.py -d $HOME/promotion/data/ecfa`

4. Perform analysis
   `python combined_analysis.py --directory $HOME/promotion/data/ecfa --mode analysis`
