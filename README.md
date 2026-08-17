# ChameleonBinder
ChameleonBinder is a method for designing small-molecule protein binders. It uses pseudo-Val residues to place ligands more precisely into binding pockets and converges with three iterative rounds of ligand-conditioned protein sequence design and structure prediction.

ChameleonBinder depends on the following tools:

- [AutoDock Vina](https://ccsb.scripps.edu/adfr/downloads/)
- [LigandMPNN](https://github.com/dauparas/LigandMPNN)
- [AlphaFold3](https://github.com/google-deepmind/alphafold3)

Please follow the installation instructions for each tool before running ChameleonBinder.

## Workflow

1. Prepare the ligand conformation from an external source, such as the PDB, or generate it with RDKit using the commands below:
`python smiles2sdf.py --ligand ligandsmiles --output ligand.sdf`  `obabel -isdf ligand.sdf -O ligand.mol2`

2. Dock the ligand against the scaffold library using the script
`bash batchdock.sh`

3. Extract complexes that meet the docking threshold, for example, those with a Vina score lower than -7 kcal/mol,
`python extract_score_and_pose_confidence.py`

4. Perform sequence design with LigandMPNN using the default parameters, then run structure prediction with AlphaFold3 as described in the manuscript.

5. Iterations to achieve self-consistency.
