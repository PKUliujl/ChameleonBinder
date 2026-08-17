
from rdkit import Chem
from rdkit.Chem import AllChem

def smiles_to_sdf(smiles: str, output_path: str) -> None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    mol = Chem.AddHs(mol)

    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    status = AllChem.EmbedMolecule(mol, params)

    if status != 0:
        raise RuntimeError("Failed to generate 3D conformer")

    optimize_status = AllChem.UFFOptimizeMolecule(mol)
    if optimize_status != 0:
        print("Warning: UFF optimization did not fully converge")

    writer = Chem.SDWriter(output_path)
    writer.write(mol)
    writer.close()

def main():
    parser = argparse.ArgumentParser(description="Convert SMILES to SDF")
    parser.add_argument("--ligand", required=True, help="Ligand SMILES string")
    parser.add_argument("--output", required=True, help="Output SDF file path")
    args = parser.parse_args()

    smiles_to_sdf(args.ligand, args.output)

if __name__ == "__main__":
    main()
