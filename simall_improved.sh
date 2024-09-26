# Boolean variable to switch between modes
# false: print commands but do not execute them
# true: execute commands and do not print them

execute_bsub=true

# further configs

outdir=$HOME/promotion/data/TEST_IMPROVED
detDirVicKekWorkServer=$HOME/promotion/code/k4geo/FCCee/ILD_FCCee/compact


source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh


for idet in {8..10}; do # detector models

    if (( $idet == 0 )); then
        # use 30mrad for the fcc models
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=/home/ilc/jeans/lcgeo-1/ILD/compact
        detmod=ILD_l5_v11beta  # this is ILD-like with FCCee MDI, inner si + ILD TPC, CALS
    elif (( $idet == 1 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=/home/ilc/jeans/lcgeo-1/ILD/compact
        detmod=ILD_l5_v11gamma  # this is ILD-like with FCCee MDI; field map from andrea
    elif (( $idet == 2 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact
        detmod=ILD_l5_v02
    elif (( $idet == 3 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact
        detmod=ILD_l5_v02_2T
    elif (( $idet == 4 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact
        detmod=ILD_l5_v03
    elif (( $idet == 5 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact
        detmod=ILD_l5_v05
    elif (( $idet == 6 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact
        detmod=ILD_l5_v03_noGraphite
    elif (( $idet == 7 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact
        detmod=ILD_l5_v05_noGraphite
    elif (( $idet == 8 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=${detDirVicKekWorkServer}
        detmod=ILD_FCCee_v01
    elif (( $idet == 9 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=${detDirVicKekWorkServer}
        detmod=ILD_FCCee_v01_fields
    elif (( $idet == 10 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=${detDirVicKekWorkServer}
        detmod=ILD_FCCee_v01_fields_noMask
    else
        echo crazy idet $idet
        exit 1
    fi

    [[ $execute_bsub == false ]] && echo && echo "$detdir $detmod" && echo


    if [ ! -d ${outdir}/$detmod ]; then
        mkdir ${outdir}/$detmod
    fi

    for iset in {0..2}; do # type of beamstrahlung: ILC250, FCC91, FCC240, ...

        for n in {1..2}; do # bunch crossing (ie guineapig "events")
            
            [[ $execute_bsub == false ]] && echo "idet $idet gpset $iset job $n"

            command="bsub -q l \"ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles /home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-${n}_Z.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ZatIP_tpcTimeKeepMC_${ddsimfile}_${detmod}.edm4hep.root --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > ${outdir}/${detmod}/out${n}.log 2>&1\""

            if (( $iset == 0 )); then
                [[ $execute_bsub == false ]] && echo $command || eval $command
            elif (( $iset == 1 )); then
                command="bsub -q l \"ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles /home/ilc/jeans/guineaPig/fromAndrea/pairs100/allAtIP_ZH/pairs-${n}_ZH.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ZHatIP_tpcTimeKeepMC_${ddsimfile}_${detmod}.emd4hep.root --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > ${outdir}/${detmod}/out${n}.log 2>&1\""
                [[ $execute_bsub == false ]] && echo $command || eval $command
            elif (( $iset == 2 )); then
                nn=${n}
                if (( $nn < 10 )); then
                    nn=00${n}
                elif (( $nn < 100 )); then
                    nn=0${n}
                fi
                command="bsub -q l \"ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles /group/ilc/users/jeans/pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.0${nn}.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ILC250_gt2mev_tpcTimeKeepMC_${ddsimfile}_${detmod}.emd4hep.root --numberOfEvents 5000 --guineapig.particlesPerEvent 250 > ${outdir}/${detmod}/out${n}.log 2>&1\""
                [[ $execute_bsub == false ]] && echo $command || eval $command
            fi
            
            [[ $execute_bsub == false ]] && echo

        done

    done

done
