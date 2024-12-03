import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dirList=["desktop-laptop","desktop-pi","local_desktop","local_laptop","local_pi"]
fileList=["Protocol_kelapa_c_controlled_device.csv","Protocol_kelapa_s_control_device.csv","Protocol_harmony_c_controlled_device.csv","Protocol_harmony_s_control_device.csv"]

# read csv
datamap={}
for dir in dirList:
    for file in fileList:
        f=open(dir+"/"+file,mode="r",encoding="utf-8")
        datamap[dir+"/"+file]=pd.read_csv(f)
        f.close()



df_kelapa=datamap["desktop-pi/Protocol_kelapa_c_controlled_device.csv"]
df_harmony=datamap["desktop-pi/Protocol_harmony_c_controlled_device.csv"]


# linestyle='--'
# colorList=["red","blue","purple"]

# [13,26]
# 13:27:2

def plot_part01():
    # pic01
    fig,bx=plt.subplots()
    df=df_kelapa
    protocol="kelapa"
    xlist=df["size"][13:27:2]
    y11list=df["phase1 cost"][13:27:2]
    y12list=df["phase2 cost"][13:27:2]
    y13list=df["total cost"][13:27:2]
    bx.plot(xlist,y11list,label=protocol+" phase1",color="red",linestyle='--',marker='.')
    bx.plot(xlist,y12list,label=protocol+" phase2",color="blue",linestyle='--',marker='.')
    bx.plot(xlist,y13list,label=protocol+" total",color="purple",linestyle='--',marker='.')
    bx.set_title('time cost of '+protocol+' protocol in different elliptic curve')
    bx.set_xlabel('different elliptic curves (Brainpool-p<x>t1)')
    bx.set_ylabel('time cost(ms)')
    bx.legend()
    bx.set_xticks(xlist)


    # pic02
    fig,bx=plt.subplots()
    df=df_harmony
    protocol="harmony"
    xlist=df["size"][13:27:2]
    y21list=df["phase1 cost"][13:27:2]
    y22list=df["phase2 cost"][13:27:2]
    y23list=df["total cost"][13:27:2]
    bx.plot(xlist,y21list,label=protocol+" phase1",color="red",linestyle='-',marker='.')
    bx.plot(xlist,y22list,label=protocol+" phase2",color="blue",linestyle='-',marker='.')
    bx.plot(xlist,y23list,label=protocol+" total",color="purple",linestyle='-',marker='.')

    bx.set_title('time cost of '+protocol+' protocol in different elliptic curve')
    bx.set_xlabel('different elliptic curves (Brainpool-p<x>t1)')
    bx.set_ylabel('time cost(ms)')
    bx.legend()
    bx.set_xticks(xlist)

    
    

    # pic03
    fig,bx=plt.subplots()
    df=df_kelapa
    protocol="kelapa"
    bx.plot(xlist,y11list,label=protocol+" phase1",color="red",linestyle='--',marker='.')
    bx.plot(xlist,y12list,label=protocol+" phase2",color="blue",linestyle='--',marker='.')
    df=df_harmony
    protocol="harmony"
    bx.plot(xlist,y21list,label=protocol+" phase1",color="red",linestyle='-',marker='.')
    bx.plot(xlist,y22list,label=protocol+" phase2",color="blue",linestyle='-',marker='.')
    bx.set_title('compare time cost of phase1 and phase2 in different protocols')
    bx.set_xlabel('different elliptic curves (Brainpool-p<x>t1)')
    bx.set_ylabel('time cost(ms)')
    bx.legend()
    bx.set_xticks(xlist)


    # pic04
    fig,bx=plt.subplots()
    df=df_kelapa
    protocol="kelapa"
    bx.plot(xlist,y13list,label=protocol+"total",color="purple",linestyle='--',marker='.')
    df=df_harmony
    protocol="harmony"
    bx.plot(xlist,y23list,label=protocol+"total",color="purple",marker='.')
    bx.set_title('compare total time cost in different protocols')
    bx.set_xlabel('different elliptic curves (Brainpool-p<x>t1)')
    bx.set_ylabel('time cost(ms)')
    bx.legend()
    bx.set_xticks(xlist)

    # pic10
    fig,bx=plt.subplots()
    bx.plot(xlist,100*(y21list/y11list),label="phase1",color="blueviolet",linestyle='-',marker='.')
    bx.plot(xlist,100*(y22list/y12list),label="phase2",color="peachpuff",linestyle='-',marker='.')
    bx.plot(xlist,100*((y21list+y22list)/(y11list+y12list)),label="total",color="cyan",linestyle='-',marker='.')
    bx.set_title('compare efficiency of different protocols')
    bx.set_xlabel('different elliptic curves (Brainpool-p<x>t1)')
    bx.set_ylabel('time cost ratio(%)')
    bx.legend()
    bx.set_xticks(xlist)

def plot_part02():
    # pic05
    color_list=["cyan","blueviolet","crimson","orange","rosybrown","peachpuff"]
    fig,bx=plt.subplots()
    for dir in dirList:
        df=datamap[dir+"/Protocol_kelapa_c_controlled_device.csv"]
        protocol="kelapa"
        xlist=df["size"][13:27:2]
        ylist=df["total cost"][13:27:2]
        bx.plot(xlist,ylist,label=dir+" : "+protocol,color=color_list[dirList.index(dir)],linestyle='--',marker='.')

        df=datamap[dir+"/Protocol_harmony_c_controlled_device.csv"]
        protocol="harmony"
        xlist=df["size"][13:27:2]
        ylist=df["total cost"][13:27:2]
        bx.plot(xlist,ylist,label=dir+" : "+protocol,color=color_list[dirList.index(dir)],linestyle='-',marker='.')
    bx.set_title('compare total time cost in different device sets')
    bx.set_xlabel('different elliptic curves (Brainpool-p<x>t1)')
    bx.set_ylabel('time cost(ms)')
    bx.legend()
    bx.set_xticks(xlist)

def plot_part03():
    fig,bx=plt.subplots()
    xlist= np.arange(0,2*len(dirList),2)
    width=0.7
    kelapa_phase1=[]
    kelapa_phase2=[]
    harmony_phase1=[]
    harmony_phase2=[]
    for dir in dirList:
        df_kelapa=datamap[dir+'/'+"Protocol_kelapa_c_controlled_device.csv"]
        kelapa_phase1.append(df_kelapa["phase1 cost"][31])
        kelapa_phase2.append(df_kelapa["phase2 cost"][31])
        df_harmony=datamap[dir+'/'+"Protocol_harmony_c_controlled_device.csv"]
        harmony_phase1.append(df_harmony["phase1 cost"][31])
        harmony_phase2.append(df_harmony["phase2 cost"][31])
    print(kelapa_phase1)
    print(kelapa_phase2)
    print(harmony_phase1)
    print(harmony_phase2)
    bx.bar(xlist-width/2,kelapa_phase1,color="turquoise",label="kelapa phase1")
    bx.bar(xlist-width/2,kelapa_phase2,bottom=kelapa_phase1,color="deepskyblue",label="kelapa phase2")
    for i in range(len(dirList)):
        height=kelapa_phase1[i]+kelapa_phase2[i]
        #bx.text(xlist-width/2,height,height,va="bottom",ha="center",fontsize=8)

    bx.bar(xlist+width/2,harmony_phase1,color="cadetblue",label="harmony phase1")
    bx.bar(xlist+width/2,harmony_phase2,bottom=harmony_phase1,color="dodgerblue",label="harmony phase2")
    for i in range(len(dirList)):
        height=harmony_phase1[i]+harmony_phase2[i]
        #bx.text(xlist+width/2,height,height,va="bottom",ha="center",fontsize=8)

    bx.set_xticks(xlist) #确定每个记号的位置
    bx.set_xticklabels(dirList)  #确定每个记号的内容
    bx.set_title('compare time cost in different device combinations')
    bx.set_xlabel('different device combinations (Ed25519)')
    bx.set_ylabel('time cost(ms)')
    bx.legend()
plot_part01()
# plot_part02()
#plot_part03()
plt.show()