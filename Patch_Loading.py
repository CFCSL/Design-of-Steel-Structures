# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:15:48 2023

@author: cfcpc2
"""
from sympy import symbols
import numpy as np

def Patch_Loading(Type, F_ED, t_w, h_w, b_f, f_yf, t_f, f_yw, gamma_M1, E, S_S, a, c):
	if S_S <= a:
		if Type == "A":
			k_F = 6 + 2 * (h_w / a)**2
		if Type == "B":
			k_F = 3.5 + 2 * (h_w / a)**2
		if Type == "C":
			k_F = 6 + 2 * ((S_S + c) / h_w)**2

		F_cr = 0.9 * k_F * E * t_w**3 / h_w

		if F_cr < F_ED:
			print('FIN! La estructura no cumple frente a patch loading')
			return None

		m1 = (f_yf * b_f) / (f_yw * t_w)

		# Initial m2 to calculate lambda_F
		m2 =0.02 * (h_w / t_f)**2
		
		# Calculate lambda_F
		if Type == "A" or Type == "B":
			l_y = S_S + 2 * t_f * (1 + np.sqrt(m1 + m2))
			if l_y>a:
				l_y=a
			
		if Type == "C":
			l_e = (k_F * E * t_w**2) / (2 * f_yw * h_w)
			if l_e>S_S+c:
				l_e=S_S+c
				
			l_y = min(l_e + t_f * np.sqrt(m1 / 2 + (l_e / t_f)**2 + m2),
					  l_e + t_f * np.sqrt(m1 + m2))
			
		#print(f'l_y={l_y}')
		F_y = f_yw * t_w * l_y
		print(f'f_y1={F_y}')

		if F_y < F_ED:
			print('FIN! La estructura no cumple frente a patch loading')
			return None

		lambda_F = np.sqrt((l_y * t_w * f_yw) / F_cr)
		print(f'lambda_F={lambda_F}')
		#Check the condition lambda_F (>0.5)
		if lambda_F <= 0.5:
			m2 = 0
			#continue
			if Type == "A" or Type == "B":
				l_y = S_S + 2 * t_f * (1 + np.sqrt(m1 + m2))
				if l_y>a:
					l_y=a
				
			if Type == "C":
				l_e = (k_F * E * t_w**2) / (2 * f_yw * h_w)
				if l_e>S_S+c:
					l_e=S_S+c
					
				l_y = min(l_e + t_f * np.sqrt(m1 / 2 + (l_e / t_f)**2 + m2),
						  l_e + t_f * np.sqrt(m1 + m2))
				
			print(f'l_y={l_y}')
			F_y = f_yw * t_w * l_y
			print(f'f_y2={F_y}')
			if F_y < F_ED:
				print('FIN! La estructura no cumple frente a patch loading')
				return None
			lambda_F = np.sqrt((l_y * t_w * f_yw) / F_cr)
		Xi_F = 0.5 / lambda_F
		if Xi_F>1.0:
			Xi_F=1.0
		F_Rd = Xi_F * F_y / gamma_M1

		if F_Rd < F_ED:
			print('FIN! La estructura no cumple frente a patch loading')
			return None

		eta_2 = F_ED / F_Rd

	else:
		print('FIN! La estructura no cumple frente a patch loading')
		return None

	return F_y,lambda_F, k_F, F_cr, m1, m2, l_y,Xi_F,F_Rd,  eta_2

# Input parameters
F_ED_val = 1415  # OK
t_w_val = 15e-3  # OK
h_w_val = 270e-3  # OK
b_f_val = 300e-3  # OK
f_yf_val = 355e3  # OK
t_f_val = 30e-3  # OK
f_yw_val = 355e3  # OK
gamma_M1_val = 1.1  # OK
E_val = 200e6  # OK
S_S_val = 300e-3  # OK
a_val = 1185e-3  # OK
c_val = 0.9

res = Patch_Loading(Type="A", F_ED=F_ED_val, t_w=t_w_val, h_w=h_w_val,
					 b_f=b_f_val, f_yf=f_yf_val, t_f=t_f_val, f_yw=f_yw_val,
					 gamma_M1=gamma_M1_val, E=E_val, S_S=S_S_val, a=a_val, c=c_val)

print(res)




# =============================================================================
# import numpy as np
# from sympy import symbols, sqrt, UnevaluatedExpr
# 
# ue = UnevaluatedExpr
# 
# F_ED, t_w, h_w, b_f, f_yf, t_f, f_yw, gamma_M1, E, S_S, a, c, epsilon, f_y = symbols(
#	 'F_ED t_w h_w b_f f_yf t_f f_yw gamma_M1 E S_S a c epsilon f_y'
# )
# 
# def Patch_Loading(Type, **kwargs):
#	 if kwargs['S_S'] > kwargs['a']:
#		 print('FIN! La estructura no cumple frente a patch loading')
#		 return None
# 
#	 k_F = 6 + 2 * ((kwargs['S_S'] + kwargs['c']) / kwargs['h_w'])**2 if Type == "C" else 6 + 2 * (kwargs['h_w'] / kwargs['a'])**2
# 
#	 F_cr = 0.9 * k_F * kwargs['E'] * kwargs['t_w']**3 / kwargs['h_w']
# 
#	 if F_cr < kwargs['F_ED']:
#		 print('FIN! La estructura no cumple frente a patch loading')
#		 return None
# 
#	 m1 = (kwargs['f_yf'] * kwargs['b_f']) / (kwargs['f_yw'] * kwargs['t_w'])
#	 m2 = 0.02 * (kwargs['h_w'] / kwargs['t_f'])**2
# 
#	 while True:
#		 if Type == "A" or Type == "B":
#			 l_y = kwargs['S_S'] + 2 * kwargs['t_f'] * (1 + np.sqrt(m1 + m2))
#		 else:
#			 l_e = (k_F * kwargs['E'] * kwargs['t_w']**2) / (2 * kwargs['f_yw'] * kwargs['h_w'])
#			 if l_e <= kwargs['S_S'] + kwargs['c']:
#				 l_y = min(l_e + kwargs['t_f'] * np.sqrt(m1 / 2 + (l_e / kwargs['t_f'])**2 + m2),
#						 l_e + kwargs['t_f'] * np.sqrt(m1 + m2))
# 
#		 F_y = kwargs['f_yw'] * kwargs['t_w'] * l_y
# 
#		 if F_y < kwargs['F_ED']:
#			 print('FIN! La estructura no cumple frente a patch loading')
#			 return None
# 
#		 lambda_F = sqrt((l_y * kwargs['t_w'] * kwargs['f_yw']) / F_cr)
# 
#		 if lambda_F <= 0.5:
#			 m2 = 0
#			 continue
# 
#		 Xi_r = 0.5 / lambda_F
#		 F_Rd = Xi_r * F_y / kwargs['gamma_M1']
# 
#		 if F_Rd < kwargs['F_ED']:
#			 print('FIN! La estructura no cumple frente a patch loading')
#			 return None
# 
#		 eta_2 = kwargs['F_ED'] / F_Rd
#		 return eta_2
# 
# 
# # Update variable names in the dictionary
# db = {'F_ED': 3556.6, 't_w': 17.5e-3, 'h_w': 734e-4, 'b_f': 300e-3,
#	   'f_yf': 355e3, 't_f': 33e-4, 'f_yw': 355e3, 'gamma_M1': 1.1,
#	   'E': 200e6, 'S_S': 0.33, 'a': 0.125, 'c': 0.33,
#	   'epsilon': 0.8136, 'f_y': 355}
# 
# eta2 = Patch_Loading(Type="A", **db)
# 
# print(eta2)
# =============================================================================
# =============================================================================
# 
# ue=UnevaluatedExpr
# 
# F_ED=symbols('F_ED')
# t_w=symbols('t_w')
# h_w=symbols('h_w')
# b_f=symbols('b_f')
# f_yf=symbols('f_yf')
# t_f=symbols('t_f')
# f_yw=symbols('f_yw')
# gamma_M1=symbols('gamma_M1')
# E=symbols('E')
# S_S=symbols('S_S')
# a=symbols('a')
# c=symbols('c')
# epsilon=symbols('epsilon')
# f_y=symbols('f_y')
# 
# 
# 
# def Patch_Loading( Type, **kwargs):
# 	#kwargs = {eval(key): UnevaluatedExpr(value) for key, value in kwargs.items()}
# 
# 	if S_S <=a:
# 		if Type=="A":
# 			k_F=6+2*(h_w/a)**2
# 		if Type=="B":
# 			k_F=3.5+2*(h_w/a)**2
# 				
# 		if Type=="C":
# 			k_F=6+2*((S_S+c)/h_w)**2
# 	
# 	
# 		F_cr=0.9*k_F*E*t_w**3/h_w
# 		
# 		if F_cr>=F_ED:
# 			m1= (f_yf*b_f)/(f_yw*t_w)
# 			
# 			# Initial values for lambda_F and m2:
# 				
# 			m2=0.02*(h_w/t_f)**2
# 			lambda_F=0.1
# 			while lambda_F<=0.5:
# 				
# 				if Type=="A" or "B":
# 					l_y=S_S+2*t_f*(1+np.sqrt(m1+m2))
# 					if l_y	<=a:
# 						F_y=f_yw*t_w*l_y
# 	
# 				else:
# 					l_e=(k_F*E*t_w**2)/(2*f_yw*h_w)
# 					if l_e<= S_S+c:
# 						l_y=min(l_e+t_f*np.sqrt(m1/2+(l_e/t_f)**2+m2), l_e+t_f*np.sqrt(m1+m2))
# 						F_y=f_yw*t_w*l_y
# 					
# 				
# 					
# 				if F_y>=F_ED:
# 					lambda_F=np.sqrt((l_y*t_w*f_yw)/F_cr)
# 					m2=0
# 			
# 			Xi_r=0.5/lambda_F
# 			if Xi_r<=1:
# 				F_Rd=Xi_r*F_y/gamma_M1
# 				if F_Rd>=F_ED:
# 					eta_2=F_ED/ F_Rd
# 					
# 					
# 	else: 
# 		print('FIN! La estructura no cumple frente a patch loading')
# 		
# 	return eta_2
# 		
# F_ED_val=3556.6
# t_w_val=17.5e-3
# h_w_val=734e-4
# b_f_val=300e-3
# f_yf_val=355e3
# t_f_val=33e-4
# f_yw_val=355e3
# gamma_M1_val=1.1
# E_val=200e6
# S_S_val=0.33
# a_val=0.125
# c_val=0.33
# epsilon_val=0.8136
# f_y_val=355
# 
# 
# 
# db={'F_ED':F_ED_val,'t_w':t_w_val, 'h_w':h_w_val,'b_f':b_f_val, 
# 		'f_yf': f_yf_val,'t_f':t_f_val,'f_yw':f_yw_val,'gamma_M1':gamma_M1_val, 'E': E_val, 'S_S': S_S_val, 'a': a_val,
# 		 'c': c_val,'epsilon': epsilon_val,'f_y': f_y_val}
# 
# eta2=Patch_Loading( Type="A", **db)
# 
# print(eta2)
# =============================================================================








