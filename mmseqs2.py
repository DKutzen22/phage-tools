import subprocess
from pathlib import Path

def run(cmd):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)

def mmseqs_cluster_to_fasta(input_fasta, out_prefix="phages_",
                            min_seq_id=0.9, coverage=0.8, cov_mode=1,
                            tmp_dir="tmp"):
 
    input_fasta = Path(f"/config/workspace/python/{input_fasta}")
    db = out_prefix + "DB"
    clu = out_prefix + "Clu"
    clu_seq = out_prefix + "Clu_seq"
    tmp_dir = Path(tmp_dir)
    tmp_dir.mkdir(exist_ok=True)

    # 1. createdb
    run(["mmseqs", "createdb", str(input_fasta), db])

    # 2. cluster
    run([
        "mmseqs", "cluster", db, clu, str(tmp_dir),
        "--min-seq-id", str(min_seq_id),
        "-c", str(coverage),
        "--cov-mode", str(cov_mode),
    ])

    # 3. createseqfiledb
    run(["mmseqs", "createseqfiledb", db, clu, clu_seq])

    # 4. result2flat -> FASTA
    out_fasta = out_prefix + "_clustered.fasta"
    run(["mmseqs", "result2flat", db, db, clu_seq, out_fasta])

    return output_fasta
