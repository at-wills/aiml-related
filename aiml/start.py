# -*- coding: utf-8 -*-
import aiml
import os

alice_path = './aiml/alice/'
# 切换到语料库所在目录
os.chdir(alice_path)
 
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond('LOAD ALICE')
 
while True:
	print alice.respond(raw_input(">> "))
