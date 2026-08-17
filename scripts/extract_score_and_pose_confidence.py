import re,os

''' 
This script extracts the docking pose to generate the initial complex structure for a given Vina score threshold (for example, a Vina score lower than -7 kcal/mol; adjust this in line 43). 
It also requires you to set the Open Babel path (line 48) on your system, specify the scaffolds repository path (line 50) and output repository path (line 57).
'''
def extract_scores(score_file):
    scores = {}
    with open(score_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('-----+------------+----------+----------'):
                start_index = lines.index(line) + 1
                break
        for line in lines[start_index:]:
            if line.startswith('   '):  # score lines start with three spaces
                parts = line.split()
                model = int(parts[0])
                score = float(parts[1])
                scores[model] = score
    return scores

##transform #babel -ipdbqt input.pdbqt -O input.pdb
def extract_conformations(pdb_file, scores):
    conformations = {}
    with open(pdb_file, 'r') as f:
        lines = f.readlines()
        model = None
        conformation = []
        for line in lines:
            if line.startswith('MODEL'):
                model = int(line.split()[1])
            elif line.startswith('ENDMDL') or line.startswith('END'):
                if model in scores:
                    conformations[model] = conformation
                conformation = []
                model = None
            elif model is not None and (line.startswith('ATOM') or line.startswith('REMARK') or line.startswith('CONECT')):
                conformation.append(line)
    return conformations

def main(score_file, conformation_file):
    scores = extract_scores(score_file)
    filtered_scores = {key: value for key, value in scores.items() if value <= -7} ## only extract higher score
    if filtered_scores:
        print(f'---------working on {score_file[:-4]}----------')
        print(filtered_scores)
        os.system(f'obabel -ipdbqt {conformation_file} -O {conformation_file[:-2]}')
        conformations = extract_conformations(conformation_file[:-2], filtered_scores)
        f = open('/path/to/Scaffolds/Helix_outs/'+score_file.split('/')[-1][:-4] + '.pdb', 'r')
        rows = f.readlines()
        f.close()
        for model, score in filtered_scores.items():
            print(f'Model: {model}, Score: {score}, Conformation:')
            print(''.join(conformations[model]))
            ##begin write files
            f = open('vina_outs_complex/' + score_file.split('/')[-1][:-4] + '_%d.pdb'%model,'w')
            for i in rows:
                if i[:4]=='ATOM':f.write(i)
            f.write(''.join(conformations[model]))
            f.close()
        print(f'---------{score_file[:-4]} completed----------\n')

if __name__ == "__main__":
    for filename in [i for i in os.listdir('vina_outs/') if i[-4:]=='.log']:
        prefix = filename[:-4]
        main( os.path.join('vina_outs/', prefix+'.log'), os.path.join('vina_outs/',prefix + '.pdbqt') )
