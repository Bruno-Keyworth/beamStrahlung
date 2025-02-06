# Very brief how-to-use

1. create env var `myCodeDir`
   its value needs to be the parent dir path of the k4geo and beamStrahlung repos (it is assumed that they are located in the same parent dir)

2. Simulate particle propagation through detector and its response
   `python simall.py -n test --detectorModel ILD_l5_v02 ILD_FCCee_v01 --scenario FCC240 FCC091 ILC250`

3. Evaluate generate data
   `python combined_analysis.py --directory $HOME/promotion/data/test --mode overview`
   or `python combined_analysis.py -n test --mode overview` if `dtDir` env var is set

   - in case of problems try: `python analyze_available_data.py -n $HOME/promotion/data/ecfa`

4. Perform analysis
   `python combined_analysis.py --directory $HOME/promotion/data/ecfa --mode analysis`
