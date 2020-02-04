# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:08:24 2020

@author: khyati
"""
def work_exp(inputlist):
    import json
    import os
    from datetime import datetime
    import operator
    #mypathh='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191129072019/TargetDocuments/'
    #mypath='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191118123425/SourceDocument/'
    mypathh='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191118123425/TargetDocuments/'
    '''
    #mypath='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191129072019/SourceDocument/'
    
    l=[]
    for f in os.listdir(mypath):
        #print(f)
        with open(mypath+f+"/"+f+".json",'r',encoding='cp850') as file:
            data=json.load(file)
            print(f)
            print(data)
            
            a=data["SovrenData"]["JobTitles"]
            
            for keys in a:
                if keys=="JobTitle":
                    for i in a["JobTitle"]:
                        if "/" in i:
                            i=i.split(" / ")
                            for j in i:
                                if j not in l:
                                    l.append(j)
                                    #print(l,"sdb")
                        else:
                            if i not in l:
                                l.append(i)
                                #print(l,"sdbc")
                else:
                    a[keys]=a[keys].split(" / ")
                    #print("dscbkh")
                    for i in a[keys]:
                        if i not in l:
                            l.append(i)
    
    '''
    l=[]
    for i in range(len(inputlist)):
        d={}
        dd={}
        for keys in inputlist[i]:
            if keys=='CategoryCode':
                d['CategoryCode']=inputlist[i]['CategoryCode']
            if keys=='Experience':
                d['Experience']=inputlist[i]['Experience']
        for keys in inputlist[i]:    
            if keys=='JobPosition':
                dd[inputlist[i]['JobPosition']]=d
        l.append(dd)    
        
    print(l)
    gd={}
    comp_str={}
    for f in os.listdir(mypathh):
        print(f)
        with open(mypathh+f+"/"+f+".json",'r',encoding='cp850') as file:
            data=json.load(file)
            #print(f)
            if 'EmploymentHistory' in data["Resume"]["StructuredXMLResume"]:
                a=data["Resume"]["StructuredXMLResume"]["EmploymentHistory"]["EmployerOrg"]
                #ll=[]
                ud={}
                comp={}
                #print(f)
                #print(len(a))
                for i in range(len(a)):
                    pos_hist_roles=[]
                    #print(a[i]["PositionHistory"][0])
                    for j in range(len(a[i]["PositionHistory"])):
                        
                        pos_hist_role={}
                        title=""
                        pht={}
                        if "StartDate" and "EndDate" in a[i]["PositionHistory"][j]:
                                
                            sdd=a[i]["PositionHistory"][j]["StartDate"]
                            for _ in sdd:
                                if _ == "YearMonth":
                                    sd=sdd["YearMonth"]
                                    
                                if _=="AnyDate":
                                    if sdd["AnyDate"]=="notKnown":
                                        break
                                    else:
                                        sd=sdd["AnyDate"]
                                if _=="Year":
                                    sd=sdd["Year"]+"-00"
                            ldd=a[i]["PositionHistory"][0]["EndDate"]
                            for _ in ldd:
                                if _ == "YearMonth":
                                    ld=ldd["YearMonth"]
                                if _=="AnyDate":
                                    ld=ldd["AnyDate"]
                                if _=="Year":
                                    ld=ldd["Year"]+"-00"
                                if _=="StringDate":
                                    currentMonth = datetime.now().month
                                    currentYear = datetime.now().year
                                    ld=str(currentYear)+"-"+str(currentMonth)
                            #print(sd,ld) 
                            pht[sd]=ld                               
                            sd=sd.split("-")
                            ld=ld.split("-")
                            sd=sd[:2]
                            ld=ld[:2]
                            nl=[]
                            
                            #print(sd,ld)
                            for _ in range(len(sd)):
                                nl.append(int(ld[_])-int(sd[_]))
                            nl[0]=nl[0]*12
                            exp=nl[0]+nl[1]
                            pht["experience"]=exp
        
                        else:
                            exp=0
                            pht["experience"]=exp
                        if "UserArea" in a[i]["PositionHistory"][j]:
                            area=a[i]["PositionHistory"][j]["UserArea"]["sov:PositionHistoryUserArea"]
                            if "sov:NormalizedTitle" in area:
                                title=area["sov:NormalizedTitle"]
                            if "sov:Subtitles" in area:
                                for _ in range(len(area["sov:Subtitles"]["sov:Subtitle"])):
                                    title=title+"/"+area["sov:Subtitles"]["sov:Subtitle"][_]
                                #ud[a[i]["PositionHistory"][0]["UserArea"]["sov:PositionHistoryUserArea"]["sov:NormalizedTitle"]]=exp
                            #print(title)
                        if "JobCategory" in a[i]["PositionHistory"][j]:
                            if len(a[i]["PositionHistory"][j]["JobCategory"])==1:
                                pht["CategoryCode"]=a[i]["PositionHistory"][j]["JobCategory"][0]["CategoryCode"]
                            elif len(a[i]["PositionHistory"][j]["JobCategory"])==2:
                                pht["CategoryCode"]=a[i]["PositionHistory"][j]["JobCategory"][1]["CategoryCode"]
                        
                        #print(pht)
                        pos_hist_role[title]=pht
                        pos_hist_roles.append(pos_hist_role)
                        #print(pos_hist_roles) 
                        #print()
                    if "UserArea" in a[i]:
                        comp[a[i]["UserArea"]["sov:EmployerOrgUserArea"]["sov:NormalizedEmployerOrgName"]]=pos_hist_roles
                    else:
                        comp[""]=pos_hist_roles
                    #print(comp)
                comp_str[f]=comp    
                gd[f]=ud
        #print(comp_str)
    for k,v in comp_str.items():
        print(k,":-",v)
        print()
      
    resd={}
    
    cat_list=["Entry Level","Experienced (non-manager)",
              "Senior (more than 5 years experience)","Manager",
              "Senior Manager (more than 5 years management experience)",
              "Executive (VP, Dept. Head)",
              "Senior Executive (President, C-level)"]    
    for i in comp_str:
        score=0
        #resl={}
        recent=1000
        exp_max=50
        print(i)
        for j in comp_str[i]:
            #print(j)
            for k in range(len(comp_str[i][j])):
                #for _ in range(len(comp_str[i][j][k])):  
                totalexp=0
                cc=0
                for title in comp_str[i][j][k]:
                    
                    for key in comp_str[i][j][k][title]:
                        if key=="experience":
                            totalexp=totalexp+comp_str[i][j][k][title][key]
                    count=0
                    if title !="":
                        resume_list=title.split("/")
                        #print(resume_list)
                        cc=cc+len(resume_list)   
                        for z in range(len(l)):
                            for zz in l[z]:
                                for jdkeys in l[z][zz]:
                                    if jdkeys=="CategoryCode":
                                        jdcc=l[z][zz]['CategoryCode']
                                    if jdkeys=='Experience':
                                        jdexp=l[z][zz]['Experience']
                                #print(jdcc,jdexp)
                                if zz!='':
                                    #print("in list")
                                    if zz in resume_list:
                                        #print(zz)
                                        count=count+1
                                        for key in comp_str[i][j][k][title]:
                                            if key!="experience" and key!="CategoryCode":
                                                 #print(key,len(key),type(comp_str[i][j][k][title][key]),"dsv ")
                                                 currentMonth = datetime.now().month
                                                 currentYear = datetime.now().year
                                                 ld=str(currentYear)+"-"+str(currentMonth)
                                                 #sd=value.split("-")
                                                 if len(key)==4:
                                                     sd=comp_str[i][j][k][title][key]+"-00"
                                                     print(sd,"fdkb")
                                                 sd=comp_str[i][j][k][title][key].split("-")
                                                 ld=ld.split("-")
                                                 #print(sd,ld)
                                                 sd=sd[:2]
                                                 ld=ld[:2]
                                                 nl=[]
                                                
                                                 #print(sd,ld)
                                                 for _ in range(len(sd)):
                                                     nl.append(int(ld[_])-int(sd[_]))
                                                 nl[0]=nl[0]*12
                                                 new_recent=nl[0]+nl[1]
                                                 if new_recent<recent:
                                                     recent=new_recent/12
                                                 #resl.append(recent)
                                                 #print(recent)
                                            if key=="experience":
                                                #print(key,"hfe wvhj")
                                                if jdexp!='':
                                                    if comp_str[i][j][k][title][key]>(int(jdexp)*12):
                                                        
                                                        score=score+50
                                                        break
                                                    if comp_str[i][j][k][title][key]<=(int(jdexp)*12):
                                                        bws=((comp_str[i][j][k][title][key]/(int(jdexp)*12))*50)
                                                        if exp_max-bws>=0:
                                                            score=score+bws
                                                            exp_max=50-bws
                                                        elif exp_max>=0 and exp_max-bws<0:
                                                            score=score+exp_max
                                                            exp_max=0
                                                if jdexp=='':
                                                    print("no exp")
                                                    if totalexp!=0:
                                                        score=score+((comp_str[i][j][k][title][key]/(totalexp))*37.5)
                                            if key=="CategoryCode":
                                                #print(key,"dskjbfk")
                                                if jdcc!='':
                                                    
                                                    if comp_str[i][j][k][title][key]>=jdcc:
                                                        
                                                        if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*10) 
                                                    if comp_str[i][j][k][title][key]<jdcc:
                                                        if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*7.5) 
                                                if jdcc=='':
                                                     print("no cat")
                                                     if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*10) 
                                    #score=(score*count)/cc
                                        print(score)
                                    if zz not in resume_list:
                                        #print(z)
                                        #print("not in list")
                                        for key in comp_str[i][j][k][title]:
                                            if key!="experience" and key!="CategoryCode":
                                                 #print(key,len(key),type(comp_str[i][j][k][title][key]),"dsv ")
                                                 currentMonth = datetime.now().month
                                                 currentYear = datetime.now().year
                                                 ld=str(currentYear)+"-"+str(currentMonth)
                                                 #sd=value.split("-")
                                                 if len(key)==4:
                                                     sd=comp_str[i][j][k][title][key]+"-00"
                                                     print(sd,"fdkb")
                                                 sd=comp_str[i][j][k][title][key].split("-")
                                                 ld=ld.split("-")
                                                 #print(sd,ld)
                                                 sd=sd[:2]
                                                 ld=ld[:2]
                                                 nl=[]
                                                
                                                 #print(sd,ld)
                                                 for _ in range(len(sd)):
                                                     nl.append(int(ld[_])-int(sd[_]))
                                                 nl[0]=nl[0]*12
                                                 new_recent=nl[0]+nl[1]
                                                 if new_recent<recent:
                                                     recent=new_recent/12
                                                 #resl.append(recent)
                                                 #print(recent)
                                            if key=="experience":
                                                #print(key,"hfe wvhj")
                                                if jdexp!='':
                                                    if comp_str[i][j][k][title][key]>(int(jdexp)*12):
                                                        score=score+50
                                                        break
                                                    if comp_str[i][j][k][title][key]<=(int(jdexp)*12):
                                                        bws=((comp_str[i][j][k][title][key]/(int(jdexp)*12))*37.5)
                                                        if exp_max-bws>=0:
                                                            score=score+bws
                                                            exp_max=50-bws
                                                        elif exp_max>=0 and exp_max-bws<0:
                                                            score=score+exp_max
                                                            exp_max=0
                                                if jdexp=='':
                                                    #print("no exp")
                                                    if totalexp!=0:
                                                        score=score+((comp_str[i][j][k][title][key]/(totalexp))*28.125)
                                            if key=="CategoryCode":
                                                #print(key,"dskjbfk")
                                                if jdcc!='':
                                                    
                                                    if comp_str[i][j][k][title][key]>=jdcc:
                                                        
                                                        if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*7.5) 
                                                    if comp_str[i][j][k][title][key]<jdcc:
                                                        if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*5.625) 
                                                if jdcc=='':
                                                     #print("no cat")
                                                     if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*7.5) 
                                    print(score)
                                #score=(score*count)/cc
                        #resl.append(score)
                        #score=(score*count)/cc 
                               
                                if zz=='':
                                    
                                    for key in comp_str[i][j][k][title]:
                                            if key!="experience" and key!="CategoryCode":
                                                 #print(key,len(key),type(comp_str[i][j][k][title][key]),"dsv ")
                                                 currentMonth = datetime.now().month
                                                 currentYear = datetime.now().year
                                                 ld=str(currentYear)+"-"+str(currentMonth)
                                                 #sd=value.split("-")
                                                 if len(key)==4:
                                                     sd=comp_str[i][j][k][title][key]+"-00"
                                                     print(sd,"fdkb")
                                                 sd=comp_str[i][j][k][title][key].split("-")
                                                 ld=ld.split("-")
                                                 #print(sd,ld)
                                                 sd=sd[:2]
                                                 ld=ld[:2]
                                                 nl=[]
                                                
                                                 #print(sd,ld)
                                                 for _ in range(len(sd)):
                                                     nl.append(int(ld[_])-int(sd[_]))
                                                 nl[0]=nl[0]*12
                                                 new_recent=nl[0]+nl[1]
                                                 if new_recent<recent:
                                                     recent=new_recent/12
                                                 #resl.append(recent)
                                                 #print(recent)
                                            if key=="experience":
                                                #print(key,"hfe wvhj")
                                                if jdexp!='':
                                                    if comp_str[i][j][k][title][key]>(int(jdexp)*12):
                                                        score=score+37.5
                                                        break
                                                    if comp_str[i][j][k][title][key]<=(int(jdexp)*12):
                                                        bws=((comp_str[i][j][k][title][key]/(int(jdexp)*12))*37.5)
                                                        if exp_max-bws>=0:
                                                            score=score+bws
                                                            exp_max=37.5-bws
                                                        elif exp_max>=0 and exp_max-bws<0:
                                                            score=score+exp_max
                                                            exp_max=0
                                                if jdexp=='':
                                                    if totalexp!=0:
                                                        score=score+((comp_str[i][j][k][title][key]/(totalexp))*28.125)
                                            if key=="CategoryCode":
                                                #print(key,"dskjbfk")
                                                if jdcc!='':
                                                    
                                                    if comp_str[i][j][k][title][key]>=jdcc:
                                                        
                                                        if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*7.5) 
                                                    if comp_str[i][j][k][title][key]<jdcc:
                                                        if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*5.625) 
                                                if jdcc=='':
                                                     if comp_str[i][j][k][title][key] in cat_list:
                                                            index=cat_list.index(comp_str[i][j][k][title][key])+1
                                                            len_l=len(cat_list)
                                                            score=score+((((index*(index+1))/2)/((len_l*(len_l+1))/2))*7.5) 
                                                         
                                    #resl.append(score)  
                                    
                        score=(score*count)/cc         
            #print(f,recent,score)
        #print(cc,count)
                        
        if recent!=1000:
            if recent==0:
                score=score+10
            else:
                score=score+(10/recent)

        resd[i]=score/len(inputlist)
    #print(resd)                            
    resd=dict( sorted(resd.items(), key=operator.itemgetter(1),reverse=True))
    return resd
                                        
print(work_exp([

{"JobPosition":"Senior Software Engineer",
"CategoryCode":"",
"Experience":"8"

},
{"JobPosition":"Technical Lead",
"CategoryCode":"",
"Experience":""

},
{"JobPosition":"Software Engineer",
"CategoryCode":"",
"Experience":""

},
{"JobPosition":"Software Development Engineer",
"CategoryCode":"",
"Experience":""

}

])  )                             
                            
                            
                    
                    
        

    
            
        
        
            
    
            
            
          
                
        
            
        
        