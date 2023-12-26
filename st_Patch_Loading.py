# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:03:08 2023

@author: cfcpc2
"""

import pandas as pd
import numpy as np
import streamlit as st
from Patch_Loading import *


import matplotlib.pyplot as plt
from PIL import Image
init_printing()


st.title('**These calculations base on the document Eurocode 3: Design of steel structures - Part 1-5:Plated structural elements**')

st.header('**Section 6: Resistance to transverse forces**')

st.markdown('---')


st.markdown('**6.1 Basis**')
st.markdown(f"""
			(1) The design resistance of the webs of rolled beams and welded girders should be determined in 
accordance with 6.2, provided that the compression flange is adequately restrained in the lateral direction.

(2) The load is applied as follows: 
	
a) through the flange and resisted by shear forces in the web, see Figure 6.1 (a); 
	
b) through one flange and transferred through the web directly to the other flange, see Figure 6.1 (b). 

c) through one flange adjacent to an unstiffened end, see Figure 6.1 (c)

(3) For box girders with inclined webs the resistance of both the web and flange should be checked. The 
internal forces to be taken into account are the components of the external load in the plane of the web and 
flange respectively. 

(4) The interaction of the transverse force, bending moment and axial force should be verified using 7.2.
			""")
			
# Load an image from file
image = Image.open("Types.png")
# Display the image
st.image(image,  use_column_width=True)

st.markdown('**6.2 Input datas**')
# Input parameters

#
F_Ed_val = st.sidebar.number_input('Design transverse force $F_{Ed} [kN]$', value= 1415.0, min_value=100.0, step=10.0, format="%.1f")
#
t_w_val = st.sidebar.number_input('thickness of the plate $t_{w} [m]$', value= 15e-3, min_value=0.0, step=0.10, format="%.3f")
#
h_w_val = st.sidebar.number_input('clear web depth between flanges $h_w [m]$', value= 270.0e-3, min_value=0.0, step=0.10, format="%.3f")

b_f_val = st.sidebar.number_input('being taken as not larger than $15\\epsilon*t_f$ on each side of the web $b_{f} [m]$', value= 300.0e-3, min_value=0.0, step=0.10, format="%.3f")

f_yf_val = st.sidebar.number_input(' the yield strength of the web $f_{yf} [kN/m^2]$', value= 355.0e3, min_value=0.10, step=0.0, format="%.3f")

t_f_val = st.sidebar.number_input('Design transverse force $F_{ED} [m]$', value= 30.0e-3, min_value=0.0, step=0.10, format="%.3f")

f_yw_val = st.sidebar.number_input(' the yield strength of the web $f_{yw} [kN/m^2]$', value= 255.0e3, min_value=0.0, step=0.10, format="%.3f")

gamma_M1_val = st.sidebar.number_input('Design transverse force $\\gamma_{M1} $', value= 1.1, min_value=0.0, step=0.01, format="%.3f")

E_val = st.sidebar.number_input('Elasticity module $E [kN/m^2]$', value= 200.0e6, min_value=1.0e6, step=1.0e6, format="%.1f")

s_s_val = st.sidebar.number_input(' $s_s [m]$', value= 300.0e-3, min_value=0.0, step=0.10, format="%.3f")

a_val = st.sidebar.number_input('length of a stiffened or unstiffened plate $a [m]$', value= 1185.0e-3, min_value=0.0, step=0.10, format="%.3f")

c_val = st.sidebar.number_input('Distance $c [m]$', value= 900e-3, min_value=0.0, step=0.10, format="%.3f")

db={'F_Ed':F_Ed_val, 't_w': t_w_val, 'h_w': h_w_val, 'b_f':b_f_val,
	"f_yf": f_yf_val, "t_f":t_f_val, "f_yw":f_yw_val, "gamma_M1": gamma_M1_val,
	"E":E_val, "s_s":s_s_val, "a":a_val, "c":c_val}


Types=["A","B","C"]

Type= st.selectbox("chose type of load applicatrion", options=Types)

if db['s_s'] < db['a']:
	st.write("The interaction of the transverse force, bending moment and axial force should be verified using 7.2.")
	st.latex(latex(k_F_func(Type)))
	st.latex(latex(k_F_func(Type, **db)))
	k_F_val=N(k_F_func(Type, **db). doit(),4)
	st.latex(latex(k_F_val))
	db['k_F']=k_F_val.rhs
	
	st.write('Transverse force:')
	st.latex(latex(F_cr_func(Type)))
	st.latex(latex(F_cr_func(Type, **db)))
	F_cr_val=N(F_cr_func(Type, **db). doit(),4)
	st.latex(latex(F_cr_val)+f'[kN]')
	db['F_cr']=F_cr_val.rhs
	
	if db['F_cr'] < db['F_Ed']:
		st.markdown("""$F_{cr}< F_{Ed}$,""")
		st.markdown("""FIN! La estructura no cumple frente a patch loading""")
	else:
		st.markdown("""Calculate $m_1$""")
		st.latex(latex(m_1_func(Type)))
		st.latex(latex(m_1_func(Type, **db)))
		m_1_val=N(m_1_func(Type, **db). doit(),4)
		st.latex(latex(m_1_val)+f'[m]')
		db['m_1']=m_1_val.rhs
		
		st.markdown("""Calculate $m_2$""")
		st.latex(latex(m_2_func(Type)))
		st.latex(latex(m_2_func(Type, **db)))
		m_2_val=N(m_2_func(Type, **db). doit(),4)
		st.latex(latex(m_2_val)+f'[m]')
		db['m_2']=m_2_val.rhs
	
		if Type=="C":
			st.latex(latex(l_e_func(Type)))
			l_e_val=N(l_e_func(Type, **db). doit(),4)
			st.latex(latex(l_e_val)+f'[m]')
			db['l_e']=l_e_val.rhs # check the conditions
			
		st.markdown("""Effective loaded length $l_y$""")	
		st.latex(latex(l_y_func(Type)))
		l_y_val=N(l_y_func(Type, **db). doit(),4)
	
		if Type=="A" or Type=="B": 
			if l_y_val.rhs>db['a']:
				st.write("but l y ≤ distance between adjacent transverse stiffeners")
				st.write(f'$l_y=$ {db["a"]} [m]')
				#l_y_val.rhs=db['a']
				db['l_y']=db['a']
				#st.latex(latex(Eq[l_y,db['a']])+f'[m]')
		st.latex(latex(l_y_val)+f'[m]')
		db['l_y']=l_y_val.rhs
		
		st.markdown("""Calculate $F_y$""")
		st.latex(latex(F_y_func(Type)))
		st.latex(latex(F_y_func(Type, **db)))
		F_y_val=N(F_y_func(Type, **db). doit(),4)
		st.latex(latex(F_y_val)+f'[kN]')
		db['F_y']=F_y_val.rhs
	
		if db['F_y'] < db['F_Ed']:
			st.markdown("""$F_y < F_{Ed}$ FIN! La estructura no cumple frente a patch loading""")
	
		st.markdown("""Calculate $\lambda_F$""")
		st.latex(latex(lambda_F_func(Type)))
		st.latex(latex(lambda_F_func(Type, **db)))
		lambda_F_val=N(lambda_F_func(Type, **db). doit(),4)
		st.latex(latex(lambda_F_val))
		db['lambda_F']=lambda_F_val.rhs

		if db['lambda_F']<=0.5:
			st.markdown("""The value of $\lambda_F=${db['lambda_F']} $< 0.5$ then we need to recalculate $m_2=0$""")
			del db['m_2']
			if 'l_e' in db.keys():
				del db['l_e']
			del db['l_y']
			del db['F_y']
			del db['lambda_F']
			st.latex(latex(Eq(m_2,0)))
			db['m_2']=0
			if Type=="C":
				st.latex(latex(l_e_func(Type)))
				st.latex(latex(l_e_func(Type, **db)))
				l_e_val=N(l_e_func(Type, **db). doit(),4)
				st.latex(latex(l_e_val)+f'[m]')
				db['l_e']=l_e_val.rhs
			st.markdown("""$l_y$ is the effective loaded length""")
			st.latex(latex(l_y_func(Type)))
			st.latex(latex(l_y_func(Type, **db)))
			l_y_val=N(l_y_func(Type, **db). doit(),4)
			st.latex(latex(l_y_val)+f'[m]')
			db['l_y']=l_y_val.rhs
			
			st.latex(latex(F_y_func(Type)))
			st.latex(latex(F_y_func(Type, **db)))
			F_y_val=N(F_y_func(Type, **db). doit(),4)
			st.latex(latex(F_y_val)+f'[kN]')
			db['F_y']=F_y_val.rhs
		
			if db['F_y'] < db['F_Ed']:
				st.markdown("""$F_y < F_{Ed}$ FIN! La estructura no cumple frente a patch loading""")
			st.latex(latex(lambda_F_func(Type)))
			st.latex(latex(lambda_F_func(Type, **db)))
			lambda_F_val=N(lambda_F_func(Type, **db). doit(),4)
			st.latex(latex(lambda_F_val))
			db['lambda_F']=lambda_F_val.rhs
			
			if db['lambda_F']<=0.5:
				st.markdown(f""" $m_2=0$,  $\lambda_F=${db['lambda_F']} $< 0.5$, does not satisfy the condition""")
			
			else:
				st.write("Reduction factor $\chi_F$ for effective length for resistance")
				st.latex(latex(chi_F_func(Type)))
				st.latex(latex(chi_F_func(Type, **db)))
				chi_F_val=N(chi_F_func(Type, **db). doit(),4)
				st.latex(latex(chi_F_val))
				db['chi_F']=chi_F_val.rhs
			
				st.latex(latex(F_Rd_func(Type)))
				st.latex(latex(F_Rd_func(Type, **db)))
				F_Rd_val=N(F_Rd_func(Type, **db). doit(),4)
				st.latex(latex(F_Rd_val))
				db['F_Rd']=F_Rd_val.rhs
		
				if db['F_Rd']<db['F_Ed']:
					st.write("$F_{Rd}< F_{Ed}$,")
					st.write('FIN! La estructura no cumple frente a patch loading')
				else:
					st.latex(latex(eta_2_func(Type)))
					st.latex(latex(eta_2_func(Type, **db)))
					eta_2_val=N(eta_2_func(Type, **db). doit(),4)
					st.latex(latex(eta_2_val))
					db['eta_2']=eta_2_val.rhs
		else:
			st.write("Reduction factor $\chi_F$ for effective length for resistance")
			st.latex(latex(chi_F_func(Type)))
			st.latex(latex(chi_F_func(Type, **db)))
			chi_F_val=N(chi_F_func(Type, **db). doit(),4)
			st.latex(latex(chi_F_val))
			db['chi_F']=chi_F_val.rhs
		
			st.latex(latex(F_Rd_func(Type)))
			st.latex(latex(F_Rd_func(Type, **db)))
			F_Rd_val=N(F_Rd_func(Type, **db). doit(),4)
			st.latex(latex(F_Rd_val))
			db['F_Rd']=F_Rd_val.rhs
		
			if db['F_Rd']<db['F_Ed']:
				st.write("$F_{Rd}< F_{Ed}$,")
				
				st.write('FIN! La estructura no cumple frente a patch loading')
			
			st.write("The verification should be performed as follows:")
			st.latex(latex(eta_2_func(Type)))
			#latex_expression=r"latex(eta_2_func(Type,**db))"
			latex_expression=latex(eta_2_func(Type,**db))
			st.latex(latex_expression)
			eta_2_val=N(eta_2_func(Type, **db). doit(),4)
			st.latex(latex(eta_2_val))
			db['eta_2']=eta_2_val.rhs
			
else:
	sst.write("$S_s> a$,")
	st.write('FIN! La estructura no cumple frente a patch loading')

