
subnum=sub010

#for i in run1.feat run2.feat run3.feat run1_fnirt.feat run2_fnirt.feat run3_fnirt.feat sm8_run1.feat sm8_run2.feat sm8_run3.feat
for i in run1.feat run2.feat run3.feat run1_fnirt.feat run2_fnirt.feat run3_fnirt.feat run1_8mm.feat run2_8mm.feat run3_8mm.feat

do

dirpth=/mnt/psychclass/394U_2010/Data/$subnum/model/${i}/

echo '<p>============================================
<p> Registration for analysis in '$dirpth'

<p>Summary registration, FMRI to standard space<br><IMG BORDER=0 SRC='$dirpth'reg/example_func2standard1.png WIDTH=100%>

<p>Registration of example_func to initial_highres
<br><a href='$dirpth'reg/example_func2initial_highres.png><IMG BORDER=0 SRC='$dirpth'reg/example_func2initial_highres.png WIDTH=2000></a>
<p>Registration of initial_highres to highres
<br><a href='$dirpth'reg/initial_highres2highres.png><IMG BORDER=0 SRC='$dirpth'reg/initial_highres2highres.png WIDTH=2000></a>
<p>Registration of example_func to highres
<br><a href='$dirpth'reg/example_func2highres.png><IMG BORDER=0 SRC='$dirpth'reg/example_func2highres.png WIDTH=2000></a>
<p>Registration of highres to standard
<br><a href='$dirpth'reg/highres2standard.png><IMG BORDER=0 SRC='$dirpth'reg/highres2standard.png WIDTH=2000></a>
<p>Registration of example_func to standard
<br><a href='$dirpth'reg/example_func2standard.png><IMG BORDER=0 SRC='$dirpth'reg/example_func2standard.png WIDTH=2000></a>
</BODY></HTML>' >> /mnt/psychclass/394U_2010/Student_Directories/sw22595/Scripts/reg_check_results.html



done
