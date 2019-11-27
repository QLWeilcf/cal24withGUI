#命令行版计算24点
def cmptlst(lst1,lst2): #比较两个列表里元素是否相同
    a=sorted(lst1)
    b=sorted(lst2)
    return a==b
def perm(lst): #input:list,[1,2,3,4]
    n=len(lst)
    if n<=1:
        return lst
    elif n==2:
        return [[lst[0],lst[1]],[lst[1],lst[0]]] #终止条件
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
def getOne():
    result=[]
    cur=[]
    while result==[]:
        cur=[]
        for i in range(4):
            cur.append(random.randint(0,14))
        result=cal24(cur)
        if len(result)>9:
            result=result[:9]
    return (result,cur)
def cmdcal24():
    import random
    print('欢迎使用命令行版24点训练器！\n## 说明：\
          - 0,每次一个题目，出题后您需要输入可以计算得到24的计算式；\n\
          - 1,当前题目未答出可多次尝试；\n- 2,仅输入a可查看答案，跳到下一题；\n\
          - 3,目前仅支持四则运算；\n- 4,输入q可退出')
    q=''
    cur=[]
    res=[]
    while q!='q':
        if res==[]:
            res,cur=getOne()
            q=input('当前题目：{0}\n输入您的答案：'.format(str(cur)))
        elif q=='a':
            print(res)
            res,cur=getOne()
            q=input('当前题目：{0}\n输入您的答案：'.format(str(cur)))
        else:
            try:
                c=re.compile(r'\d+').findall(q)
                if len(c)!=4:
                    q=input('式子有问题，请检查后重新输入\n')
                else:
                    cr=[str(i) for i in cur]
                    if cmptlst(c,cr):
                        c=eval(q)
                        if abs(c-24)<1e-6:
                            print('计算正确！')
                            res,cur=getOne()
                            q=input('当前题目：{0}\n输入您的答案：'.format(str(cur)))
            except Exception as e:
                print(e)
                q=input('输入您的答案：'.format(str(cur)))

if __name__ == '__main__':
    cmdcal24()
