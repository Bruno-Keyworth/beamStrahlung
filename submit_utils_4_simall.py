import subprocess


def submit_job(system_type, executable, arguments, outName, sub_jobs):
    """Prepare and submit a job using the chosen batch system."""
    if system_type == "condor":
        # Create the Condor submit script
        condor_script_content = f"""Universe   = vanilla
            Executable = {executable}
            Arguments  = {" ".join(arguments)}
            Log        = {outName}.log
            Output     = {outName}.out
            Error      = {outName}.err
            Queue
            """
        condor_submit_file = outName.with_suffix(".condor")
        with open(condor_submit_file, "w", encoding="utf-8") as f:
            f.write(condor_script_content)

        condor_command = f"condor_submit {condor_submit_file}"
        if sub_jobs:
            subprocess.run(condor_command, shell=True, check=True)
        else:
            print(condor_command, end="\n\n")
    else:
        # Use bsub submission
        bsub_command = f'bsub -q l "{executable} {" ".join(arguments)}"'
        if sub_jobs:
            subprocess.run(bsub_command, shell=True, check=True)
        else:
            print(bsub_command, end="\n\n")
