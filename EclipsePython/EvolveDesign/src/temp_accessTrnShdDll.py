'''
Created on 09.06.2011

@author: mjones
'''
import ctypes

# Load DLL into memory.

path = r"D:\Programme\Trnsys17\Building\trnshdbui.dll"

hllDll = ctypes.WinDLL (path)
