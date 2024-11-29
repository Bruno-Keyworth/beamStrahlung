import subprocess


def submit_job(system_type, executable, arguments, output_file_base_name, sub_jobs):
    """Prepare and submit a job using the chosen batch system."""
    if system_type == "condor":
        # Create the Condor submit script
        condor_params = {
            "Universe": "vanilla",
            "Executable": executable,
            "Arguments": " ".join(arguments),
            "Log": f"{output_file_base_name}.log",
            "Output": f"{output_file_base_name}.out",
            "Error": f"{output_file_base_name}.err",
        }

        # Create the script content using the dictionary
        condor_script_content = (
            "\n".join(f"{key} = {value}" for key, value in condor_params.items())
            + "\nQueue\n"
        )
        condor_submit_file = output_file_base_name.with_suffix(".condor")
        with open(condor_submit_file, "w", encoding="utf-8") as f:
            f.write(condor_script_content)

        condor_command = f"condor_submit {condor_submit_file}"
        if sub_jobs:
            subprocess.run(condor_command, shell=True, check=True)
        else:
            print(condor_command, end="\n\n")

    else:
        # Use bsub submission (used at KEK)
        bsub_command = f'bsub -q l "{executable} {" ".join(arguments)}"'
        if sub_jobs:
            subprocess.run(bsub_command, shell=True, check=True)
        else:
            print(bsub_command, end="\n\n")
