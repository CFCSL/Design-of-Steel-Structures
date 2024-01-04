# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 11:11:53 2024

@author: cfcpc2
"""


import streamlit as st


st. subheader('datas')

a=3
b=5
c=6

options=["calculations"]

section_62 = st.checkbox(options[0])

if section_62:
#st.subheader("calculations")
	
	N= a+b
	
	M=a*b*c
	
	st.markdown("""N={N}""")
	st.markdown("""M={M}""")


st.subheader('Summary Results')

st. markdown("""
			 $M= {M}$
			 
			 $N={N}$
			 
			 """)

