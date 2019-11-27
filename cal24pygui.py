#发布版
import random
import tkinter as tk
from tkinter import messagebox
def perm(lst): #input:list,[1,2,3,4]
    n=len(lst)
    if n<=1: #终止条件1
        return lst
    elif n==2:
        return [[lst[0],lst[1]],[lst[1],lst[0]]] #终止条件2
    kk=[]
    for i in range(n):
        nlst=lst[0:i]+lst[i+1:] #除lst[i]外的元素
        c=perm(nlst)
        ss=[]
        for j in c:
            sw=[lst[i]]
            sw.extend(j)
            ss.append(sw)
        kk.extend(ss) #注意是extend不是append
    return kk
def cal24(a): #24点计算
    lst=[[i,''] for i in a]
    d1=perm(lst)  #len==24
    ev=['+','-','*','/']
    res=[]
    i=0
    for d in d1: #len(d)==4
        for e1 in ev: #24*4
            if e1=='/' and d[1][0]==0:
                i+=1
                continue
            r='({0}{1}{2})'.format(d[0][0],e1,d[1][0])
            
            k1=[[eval(r),r],d[2],d[3]]  #k1=[eval(),d[2],d[3]]  k1.extend(d[2:])
            d2=perm(k1) #len(k1)==3  len(d2)==A(3,2)=6
            for d3 in d2: #len(d3)==3
                for e2 in ev:
                    if e2=='/' and d3[1][0]==0:
                        i+=1
                        continue
                    r1='{0}{1}{2}'.format(d3[0][0],e2,d3[1][0])
                    y0=d3[0][0] if d3[0][1]=='' else d3[0][1]
                    y1=d3[1][0] if d3[1][1]=='' else d3[1][1]
                    r2='({0}{1}{2})'.format(y0,e2,y1)
                    k2=[[eval(r1),r2],d3[2]] # k2.extend(d3[2:]) 
                    d4=[[k2[0],k2[1]],[k2[1],k2[0]]]
                    for d5 in d4:
                        for e3 in ev:
                            if e3=='/' and d5[1][0]==0:
                                i+=1
                                continue
                            k3=eval('{0}{1}{2}'.format(d5[0][0],e3,d5[1][0]))
                            i+=1
                            if abs(k3-24)<1e-6:
                                y0=d5[0][0] if d5[0][1]=='' else d5[0][1]
                                y1=d5[1][0] if d5[1][1]=='' else d5[1][1]
                                rss='({0}{1}{2})'.format(y0,e3,y1)
                                k4=eval(rss)
                                if abs(k4-24)<1e-6:
                                    res.append(rss)
    return list(set(res))

## GUI部分
root=tk.Tk()
root.geometry('280x320+400+100') #大小和位置  widthxheight+x+y
root.title('cal 24')
ctv=tk.StringVar(root,'')
btnUs=tk.IntVar(root,0)
cur=[]
result=[]
for i in range(100):
    cur=[]
    for _ in range(4):
        cur.append(random.randint(0,10))
    ch=cur.copy()
    result=cal24(ch)
    if result!=[]:
        if len(result)>9: #只取前10个答案
            result=result[:9]
        break

if result==[]:
    for _ in range(4):
        cur.append(random.randint(0,10))
cur.append('') #对应各个按钮当前值
scur=cur.copy() #重来 用
stk=[['',''],'',['',''],'']  #操作符点击
itv=tk.StringVar(root,'---')
infov=tk.Label(root,textvariable=itv) #显示信息用 
infov.place(x=170,y=5,width=120,height=20)
#ct['state']='readonly'

stk[3]=tk.Button(root,text='').cget("background")  #默认按钮背景色 linux: #d9d9d9 win:SystemButtonFace
#回调函数
def btnClick(btn,bt=''): #btn:按下的按钮   bt:所按下按钮的标识，主要是数值键用
    global cur,stk,scur,result
    ith=itv.get()
    btnus=btnUs.get()
    uop=[i for i in range(15)] #[0,14]
    opw=['+','-','*','/']
    if btn=='--':return
    if btn in uop: #按的是数值类型的键
        btnn=cur[bt-1]
        itv.set('{0}'.format(btnn))
        if stk[0][0]=='': #第一次按到数值键
            stk[0]=[btnn,bt]  #or stk[0][0]=btnn;stk[0][1]=bt
        elif stk[1]=='':#没有按过符号键
            if stk[0][0] !='':#如两次点到数值键
                stk[0]=[btnn,bt]
        elif stk[1]!='': #关键 完成了 a+b的输入
            stk[2]=[btnn,bt]
            btnus+=1 #在这个if条件下会合并两个按钮为一个，用掉一个按钮
            vss='{0}{1}{2}'.format(stk[0][0],stk[1],stk[2][0]) #a+b

            cur[4]='({0})'.format(vss)
            #暂时不好区分是cur[4],stk[1],stk[2][0] 还是 stk[0][0],stk[1],cur[4]
            v=eval(vss)
            itv.set(vss)
            ccv=float("%.3f" %v)
            if abs(v-ccv)<1e-6:
                setVBtnval(v,bt)
            else:
                setVBtnval(ccv,bt)
            setVBtnCol('#808080',stk[0][1]) #“失效”一个按钮
            setVBtnval('--',stk[0][1])
            stk[0][0]=v
            stk[0][1]=bt
            stk[1]='' #置空后两步操作，第一步更新为v的值，以方便实现a*b+c (a+b)*c
            stk[2]=['','']
            if abs(v-24)<1e-6:
                if btnus==3: #用掉三个，结果正确，到达endgame
                    messagebox.showinfo(str(scur[:4]),'恭喜你计算正确！')
    elif btn in opw: #操作符，更新stk[1]
        if stk[0][0]=='':
            itv.set('操作符前没有数值')
            return #无效  操作符前没有数值
        elif stk[1] in opw: #覆盖上一步点的操作符
            stk[1]=btn
        elif stk[1]=='': #当前循环还没有输入过运算符
            stk[1]=btn
    elif btn=='C': #清空操作重来
        itv.set('--')
        cur=scur.copy()
        updateVBtn(cur) #更新数值按钮上的值
        resetVBtnColor(stk[3]) #重设按钮的背景色
        stk=resetStk(stk) #重设stk的值
        btnus=0 #按钮使用数重设为0
    elif btn=='Next': #下一题
        ch=[]
        for i in range(150):
            ch=[]
            for _ in range(4):
                ch.append(random.randint(0,10))
            result=cal24(ch)
            if result!=[]:
                if len(result)>9: #只取前10个答案
                    result=result[:9]
                break
        if ch==[]:
            for i in range(4):
                cur[i]=random.randint(0,10)
        else:
            for i in range(4):
                cur[i]=ch[i]
        cur[4]=''
        updateVBtn(cur)
        resetVBtnColor(stk[3])
        stk=resetStk(stk)
        scur=cur.copy()
        itv.set('--')
        btnus=0
    btnUs.set(btnus)
    #print(btnus,btn,cur,stk)

def resetStk(stk):
    stk[0]=['','']
    stk[1]=''
    stk[2]=['','']
    stk[3]=tk.Button(root,text='').cget("background")
    return stk
def updateVBtn(cur):
    btn1['text']=cur[0]
    btn2['text']=cur[1]
    btn3['text']=cur[2]
    btn4['text']=cur[3]
    
def resetVBtnColor(org):
    btn1.configure(background=org)
    btn2.configure(background=org)
    btn3.configure(background=org)
    btn4.configure(background=org)
def setVBtnCol(col,bt=''):
    if bt=='':
        return
    elif bt==1:
        btn1.configure(background=col)
    elif bt==2:
        btn2.configure(background=col)
    elif bt==3:
        btn3.configure(background=col)
    elif bt==4:
        btn4.configure(background=col)
def setVBtnval(v,bt=''):
    vt=str(v)
    if bt=='':
        return
    elif bt==1:
        btn1['text']=vt
    elif bt==2:
        btn2['text']=vt
    elif bt==3:
        btn3['text']=vt
    elif bt==4:
        btn4['text']=vt
    cur[bt-1]=v

def showAnswer(): #用消息框展示当前题目的答案
    global result,cur
    #if len(result)>9:result=result[:9] 只展示前10个答案，语句整合到算答案里了，省些存储
    rss='\n'.join([str(i) for i in result])
    messagebox.showinfo(str(cur),rss)

btn1=tk.Button(root,text=str(cur[0]),command=lambda x=cur[0]:btnClick(x,1))
btn1.place(x=0,y=10,width=90,height=90)
btn2=tk.Button(root,text=str(cur[1]),command=lambda x=cur[1]:btnClick(x,2))
btn2.place(x=90,y=10,width=90,height=90)
btn3=tk.Button(root,text=str(cur[2]),command=lambda x=cur[2]:btnClick(x,3))
btn3.place(x=0,y=100,width=90,height=90)
btn4=tk.Button(root,text=str(cur[3]),command=lambda x=cur[3]:btnClick(x,4))
btn4.place(x=90,y=100,width=90,height=90)

btn5=tk.Button(root,text='+',command=lambda :btnClick('+'))
btn5.place(x=0,y=200,width=40,height=20)
btn6=tk.Button(root,text='-',command=lambda :btnClick('-'))
btn6.place(x=45,y=200,width=40,height=20)
btn7=tk.Button(root,text='*',command=lambda :btnClick('*'))
btn7.place(x=90,y=200,width=40,height=20)
btn8=tk.Button(root,text='÷',command=lambda :btnClick('/'))
btn8.place(x=135,y=200,width=40,height=20)

btnClear=tk.Button(root,text='重来',command=lambda :btnClick('C'))
btnClear.place(x=0,y=250,width=60,height=20)
btnCompute=tk.Button(root,text='答案',command=showAnswer)
btnCompute.place(x=70,y=250,width=60,height=20)
btnNext=tk.Button(root,text='下一题',command=lambda :btnClick('Next'))
btnNext.place(x=140,y=250,width=60,height=20)

root.mainloop()
