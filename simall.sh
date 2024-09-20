# this one works
# source /cvmfs/ilc.desy.de/sw/x86_64_gcc103_centos7/v02-03/init_ilcsoft.sh
# source /cvmfs/ilc.desy.de/sw/x86_64_gcc103_centos7/v02-03-01/init_ilcsoft.sh
# source /home/ilc/jeans/tpc-ion/init_ilcsoft.sh

# source /home/ilc/jeans/tpc-ion/init_ilcsoftv02-03-01.sh

source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh

for idet in {8..10}; do # detector models

    if (( $idet == 0 )); then

        # use 30mrad for the fcc models
        ddsimfile=keep_microcurlers_10MeV_30mrad
        # detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/FCCee/compact ; detmod=FCCee_o1_v04_TPC
        # detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/FCCee/compact ; detmod=FCCee_o1_v04_TPC_noMDI
        # detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/FCCee/compact ; detmod=FCCee_o1_v04_TPC_noMDILumi
        # detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-18/FCCee/compact ; detmod=FCCee_o1_v04
        # detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-18/FCCee/compact ; detmod=FCCee_o1_v05
        # detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-18/FCCee/compact ; detmod=FCCee_o2_v02
        detdir=/home/ilc/jeans/lcgeo-1/ILD/compact ; detmod=ILD_l5_v11beta  # this is ILD-like with FCCee MDI, inner si + ILD TPC, CALS

    elif (( $idet == 1 )); then

        # use 30mrad for the fcc models
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=/home/ilc/jeans/lcgeo-1/ILD/compact ; detmod=ILD_l5_v11gamma  # this is ILD-like with FCCee MDI; field map from andrea

    elif (( $idet == 2 )); then

        # lcgeo-00-16-08 now all have dedicated beam pipe limits
        # and 14mrad for the ILD ones
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_v02
    elif (( $idet == 3 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_v02_2T
    elif (( $idet == 4 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_v03 # mag field map NO ANTIDID -> and beam pipe limits   (use long queue!)
    elif (( $idet == 5 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_v05 # mag field map WITH ANTIDID -> and beam pipe limits (use long queue!)
    elif (( $idet == 6 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_v03_noGraphite # no graphite in front of beamcal
    elif (( $idet == 7 )); then
        ddsimfile=keep_microcurlers_10MeV
        detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_v05_noGraphite # no graphite in front of beamcal

    elif (( $idet == 8 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=/home/ilc/jeans/k4geo_GH/FCCee/ILD_FCCee/compact ; detmod=ILD_FCCee_v01 # ILD_FCCee_v01, uniform field

    elif (( $idet == 9 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=/home/ilc/jeans/k4geo_GH/FCCee/ILD_FCCee/compact ; detmod=ILD_FCCee_v01_field # ILD_FCCee_v01, field map

    elif (( $idet == 10 )); then
        ddsimfile=keep_microcurlers_10MeV_30mrad
        detdir=/home/ilc/jeans/k4geo_GH/FCCee/ILD_FCCee/compact ; detmod=ILD_FCCee_v01_field_nomask # ILD_FCCee_v01, field map, no shielding

    else
        echo crazy idet $idet
        exit 1
    fi

    ## detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_vONLYTPCFCC
    ## detdir=/home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact ; detmod=ILD_l5_vTPCFCC < same as ILD_l5_v02_2T

    echo $detdir $detmod

    outdir=$HOME/promotion/data/TEST

    if [ ! -d ${outdir}/$detmod ]; then
        mkdir ${outdir}/$detmod
    fi

    for iset in {0..2}; do # type of beamstrahlung: ILC250, FCC91, FCC240, ...

        for n in {1..2}; do # bunch crossing (ie guineapig "events")
        # for n in {400..1313}; do

            echo idet $idet gpset $iset job $n

            # ddsim expects .pairs extension
            # ln -sf /home/ilc/jeans/guineaPig/fromAndrea/pairs100/fetch_Z/pairs_${n}.dat inputlinks/pairs-${n}_Z.pairs
            # ln -sf /home/ilc/jeans/guineaPig/fromAndrea/pairs/Z/pairs-${n}_Z.dat pairs-${n}_Z.pairs

            #    bsub -q s "ddsim --steeringFile ./ddsim_keep_microcurlers_10MeV.py --compactFile /home/ilc/jeans/tpc-ion/lcgeo-00-16-08/ILD/compact/${detmod}/${detmod}.xml --inputFiles pairs-${n}_Z.pairs --outputFile pairs-${n}_Z_microcurlers_10MeV_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > out${n}.log 2>&1"

            # start at nominal position given by GP
            #    bsub -q s "ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles inputlinks/pairs-${n}_Z.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_Z_tpcTimeKeepMC_${ddsimfile}_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > ${outdir}/${detmod}/out${n}.log 2>&1"

            # extrapolate pairs to near IP
            #     bsub -q l "ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles input_extrToIp/pairs-${n}_Z.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ZextIP_tpcTimeKeepMC_${ddsimfile}_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > ${outdir}/${detmod}/out${n}.log 2>&1"


            if (( $iset == 0 )); then
                # start all at IP
                # 91 GeV
                echo bsub -q l "ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles input_allatip/pairs-${n}_Z.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ZatIP_tpcTimeKeepMC_${ddsimfile}_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > ${outdir}/${detmod}/out${n}.log 2>&1"

            elif (( $iset == 1 )); then

                # 240 GeV
                echo bsub -q l "ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles /home/ilc/jeans/guineaPig/fromAndrea/pairs100/allAtIP_ZH/pairs-${n}_ZH.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ZHatIP_tpcTimeKeepMC_${ddsimfile}_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent -1 > ${outdir}/${detmod}/out${n}.log 2>&1"

            elif (( $iset == 2 )); then


                # 250 GeV

                nn=${n}
                if (( $nn < 10 )); then
                    nn=00${n}
                elif (( $nn < 100 )); then
                    nn=0${n}
                fi
                # bsub -q l "ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles /hsm/ilc/grid/storm/prod/ilc/mc-opt-3/generated/250-SetA/eepairs/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4.I270000.0${nn}.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ILC250_tpcTimeKeepMC_${ddsimfile}_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent 250 > ${outdir}/${detmod}/out${n}.log 2>&1"

                # use these for v03, v05 models (field map)
                echo bsub -q l "ddsim --steeringFile ./ddsim_${ddsimfile}.py --compactFile ${detdir}/${detmod}/${detmod}.xml --inputFiles /group/ilc/users/jeans/pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.0${nn}.pairs --outputFile ${outdir}/${detmod}/pairs-${n}_ILC250_gt2mev_tpcTimeKeepMC_${ddsimfile}_${detmod}.slcio --numberOfEvents 5000 --guineapig.particlesPerEvent 250 > ${outdir}/${detmod}/out${n}.log 2>&1"

		
		
            fi

        done

    done

done
