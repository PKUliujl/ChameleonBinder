#!/usr/bin/bash
#modify `/path/to/` to your own path.

mkdir vina_outs/

for file in $(ls /path/to/scaffolds/);do
    name=`echo $file|sed 's/.pdb//g'`
    if [ ! -f vina_outs/${name}.pdbqt ];then
        python /path/to/yourscript/Val_builder_sameorder.py /path/to/scaffolds/$file A $file
        centers=`bash /path/to/your/scripts/centerCA.sh $file`
        xx=`echo $centers|awk '{print $2}'`;
        yy=`echo $centers|awk '{print $3}'`;
        zz=`echo $centers|awk '{print $4}'`;
        /path/to/ADFRsuite_x86_64Linux_1.0/bin/prepare_receptor -r $file
        /path/to/autodock_vina_1_1_2_linux_x86/bin/vina --receptor ${name}.pdbqt --ligand your_ideal.pdbqt --config /path/to/config.txt --log vina_outs/${name}.log --center_x $xx --center_y $yy --center_z $zz --out vina_outs/${name}.pdbqt
        rm ${name}.* -fo
        echo "====================== ${name} completed ======================"
    fi
done
