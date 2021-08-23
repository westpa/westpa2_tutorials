#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT

#RMSD=$(mktemp)

COMMAND="         parm $WEST_SIM_ROOT/common_files/basis_all.prmtop\n"
COMMAND="$COMMAND trajin $WEST_STRUCT_DATA_REF \n"
COMMAND="$COMMAND reference $WEST_SIM_ROOT/reference/1brs_cg_eq2_resolv.pdb [reference] \n"
COMMAND="$COMMAND autoimage \n"
COMMAND="$COMMAND rms RMS_BN :1-110 reference out RMS_BN.dat \n"
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
COMMAND="$COMMAND secstruct Secondary_Struct_BN out Secondary_Struct_BN.dat :1-110 \n"
COMMAND="$COMMAND secstruct Secondary_Struct_BS out Secondary_Struct_BS.dat :111-199 \n"
COMMAND="$COMMAND nativecontacts name Num_Contacts :1-110 :111-199 byresidue mindist distance 4.5 out Num_Contacts.dat ref [reference] \n"
COMMAND="$COMMAND go\n"

echo -e "${COMMAND}" | ${CPPTRAJ_BASE}

cat RMS_BS_D.dat | tail -n +2 | awk {'print $2'} > $WEST_PCOORD_RETURN
#paste <(cat RMS_Helix2.dat | tail -n +2 | awk {'print $2'}) <(cat RMS_Helix3.dat | tail -n +2 | awk {'print $2'}) > $WEST_PCOORD_RETURN

#rm $RMSD
rm RMS_BS.dat RMS_BN.dat #RMS_BS_D.dat 
rm RMS_BS35.dat RMS_BS39.dat RoG.dat RoG_BN.dat RoG_BS.dat RMS_Heavy.dat RMS_Backbone.dat
rm Total_SASA.dat BN_SASA.dat BS_SASA.dat Secondary_Struct_BN.dat Secondary_Struct_BS.dat Num_Contacts.dat Secondary_Struct_BN.dat.sum Secondary_Struct_BS.dat.sum

if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi
