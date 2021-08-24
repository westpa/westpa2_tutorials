#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

ln -sv $WEST_SIM_ROOT/common_files/basis_all.prmtop .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md_WT4.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.rst ./parent.rst
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md_WT4.in > md.in
  ln -sv $WEST_PARENT_DATA_REF ./parent.rst
fi

export CUDA_DEVICES=(`echo $CUDA_VISIBLE_DEVICES_ALLOCATED | tr , ' '`)
export CUDA_VISIBLE_DEVICES=${CUDA_DEVICES[$WM_PROCESS_INDEX]}

echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES_ALLOCATED = " $CUDA_VISIBLE_DEVICES_ALLOCATED
echo "RUNSEG.SH: WM_PROCESS_INDEX = " $WM_PROCESS_INDEX
echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES = " $CUDA_VISIBLE_DEVICES

$PMEMD -O -i md.in   -p basis_all.prmtop  -c parent.rst \
          -r seg.rst -x seg.nc      -o seg.log    -inf seg.nfo

#RMSD=$(mktemp)

COMMAND="         parm $WEST_SIM_ROOT/common_files/basis_all.prmtop\n"
COMMAND="$COMMAND trajin ./parent.rst \n"
COMMAND="$COMMAND trajin $WEST_CURRENT_SEG_DATA_REF/seg.nc \n"
COMMAND="$COMMAND reference $WEST_SIM_ROOT/reference/1brs_cg_eq2_resolv.pdb [reference] \n"
COMMAND="$COMMAND autoimage \n"
COMMAND="$COMMAND rms RMS_BN :1-110 reference out RMS_BN.dat \n"
COMMAND="$COMMAND vector CoM center :111-199 out CoM.dat \n"
COMMAND="$COMMAND rms RMS_BS (:111-199) reference out RMS_BS.dat nofit \n"
COMMAND="$COMMAND rms RMS_BS_D :145,149 reference out RMS_BS_D.dat nofit \n"
COMMAND="$COMMAND rms RMS_BS_D35 :145 reference out RMS_BS35.dat nofit \n"
COMMAND="$COMMAND rms RMS_BS_D39 :149 reference out RMS_BS39.dat nofit \n"
COMMAND="$COMMAND rms RMS_Heavy (:1-199) reference out RMS_Heavy.dat \n"
COMMAND="$COMMAND rms RMS_Backbone (:1-199)&(@GC,GN,GO) reference out RMS_Backbone.dat \n"
COMMAND="$COMMAND radgyr RoG_BN :1-110 out RoG_BN.dat \n"
COMMAND="$COMMAND radgyr RoG_BS :111-199 out RoG_BS.dat \n"
COMMAND="$COMMAND radgyr RoG :1-199 out RoG.dat \n"
COMMAND="$COMMAND surf Total_SASA :1-199 out Total_SASA.dat \n"
COMMAND="$COMMAND surf BN_SASA :1-110 out BN_SASA.dat \n"
COMMAND="$COMMAND surf BS_SASA :111-199 out BS_SASA.dat \n"
COMMAND="$COMMAND secstruct Secondary_Struct_BN out Secondary_Struct_BN.dat :1-110 \n"
COMMAND="$COMMAND secstruct Secondary_Struct_BS out Secondary_Struct_BS.dat :111-199 \n"
COMMAND="$COMMAND nativecontacts name Num_Contacts_res :1-110 :111-199 mindist distance 4.5 out Num_Contacts.dat ref [reference] \n"
COMMAND="$COMMAND go\n"

echo -e "${COMMAND}" | $CPPTRAJ

#COMMAND="         parm $WEST_SIM_ROOT/common_files/basis_all.prmtop\n"
#COMMAND="$COMMAND trajin $WEST_CURRENT_SEG_DATA_REF/seg.nc \n"
#COMMAND="$COMMAND strip :WAT \n"
#COMMAND="$COMMAND trajout $WEST_CURRENT_SEG_DATA_REF/seg-nowat.nc \n"
#COMMAND="$COMMAND go\n"

#echo -e "${COMMAND}" | $CPPTRAJ

#cat $RMSD | tail -n +2 | awk '{print $2}' > $WEST_PCOORD_RETURN
#paste <(cat RMS_BN_D.dat | tail -n +2 | awk '{print $2}') > $WEST_PCOORD_RETURN
#cat RMS_BS_D.dat | tail -n +2 | awk '{print $2}' > $WEST_PCOORD_RETURN

paste <(cat RMS_BN_D.dat | tail -n +2 | awk '{print $2}')i < (cat Num_Contacts.dat | tail -n +2 | awk '{print $4}') > $WEST_PCOORD_RETURN

cat RMS_Backbone.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BACKBONE_RETURN
cat RoG.dat | tail -n +2 | awk '{print $2}' > $WEST_ROG_RETURN
cat RoG_BN.dat | tail -n +2 | awk '{print $2}' > $WEST_ROG_BN_RETURN
cat RoG_BS.dat | tail -n +2 | awk '{print $2}' > $WEST_ROG_BS_RETURN

cat CoM.dat | tail -n + 2 | awk '{print $2, $3, $4}' > $WEST_COM_RETURN

cat RMS_BN.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BN_RETURN
cat RMS_BS.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BS_RETURN
cat RMS_BS_D.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BS_D_RETURN

cat RMS_BS35.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BS35_RETURN
cat RMS_BS39.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BS39_RETURN
cat RMS_Backbone.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_BACKBONE_RETURN
cat RMS_Heavy.dat | tail -n +2 | awk '{print $2}' > $WEST_RMS_HEAVY_RETURN

cat BN_SASA.dat | tail -n +2 | awk '{print $2}' > $WEST_BN_SASA_RETURN
cat BS_SASA.dat | tail -n +2 | awk '{print $2}' > $WEST_BS_SASA_RETURN
cat Total_SASA.dat | tail -n +2 | awk '{print $2}' > $WEST_TOTAL_SASA_RETURN
cat Secondary_Struct_BN.dat | tail -n +2 | awk '{print $7}' > $WEST_SECONDARY_STRUCT_BN_RETURN
cat Secondary_Struct_BS.dat | tail -n +2 | awk '{print $7}' > $WEST_SECONDARY_STRUCT_BS_RETURN
cat Num_Contacts.dat | tail -n +2 | awk '{print $2}' > $WEST_NUM_CONTACTS_RETURN

cat Num_Contacts.dat | tail -n +2 | awk -v c=1011 '{print $2/c}' > $WEST_PERCENT_CONTACTS_RETURN


# Clean up
rm basis_all.prmtop
rm RMS_BS.dat RMS_BN.dat RMS_BS_D.dat
rm RMS_BS35.dat RMS_BS39.dat RoG.dat RoG_BN.dat RoG_BS.dat RMS_Heavy.dat RMS_Backbone.dat
rm Total_SASA.dat BN_SASA.dat BS_SASA.dat Secondary_Struct_BN.dat Secondary_Struct_BS.dat Num_Contacts.dat Secondary_Struct_BN.dat.sum Secondary_Struct_BS.dat.sum CoM.dat


#if [ -f "seg-nowat.nc" ]; then
#    rm seg.nc && 
#    mv seg-nowat.nc seg.nc
#fi

#rm -f $RMS
