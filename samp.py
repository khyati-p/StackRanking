# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:08:24 2020

@author: khyati
"""
def function(inputlist):
    import json
    import os
    from datetime import datetime
    import operator
    
    #mypath='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191118123425/SourceDocument/'
    mypathh='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191118123425/TargetDocuments/'
    '''
    #mypath='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191129072019/SourceDocument/'
    #mypathh='C:/Users/khyati/Downloads/Stack Ranking/SovrenProductDemo-BimetricScoring-20191129072019/TargetDocuments/'
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
        #print(i)
        for j in comp_str[i]:
            #print(j)
            for k in range(len(comp_str[i][j])):
                #for _ in range(len(comp_str[i][j][k])):             
                for title in comp_str[i][j][k]:
                    if title !="":
                        resume_list=title.split("/")
                        #print(resume_list)
                        for z in range(len(l)):
                            for zz in l[z]:
                                for jdkeys in l[z][zz]:
                                    if jdkeys=="CategoryCode":
                                        jdcc=l[z][zz]['CategoryCode']
                                    if jdkeys=='Experience':
                                        jdexp=l[z][zz]['Experience']
                                #print(jdcc,jdexp)
                                if zz in resume_list:
                                    #print(z)
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
                                            bws=((comp_str[i][j][k][title][key]/(jdexp*12))*50)
                                            
                                            if exp_max-bws>=0:
                                                score=score+bws
                                                exp_max=50-bws
                                            elif exp_max>=0 and exp_max-bws<0:
                                                score=score+exp_max
                                                exp_max=0
                                        if key=="CategoryCode":
                                            #print(key,"dskjbfk")
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
                                    #resl.append(score)   
            #print(f,recent,score)
        if recent!=1000:
            if recent==0:
                score=score+10
            else:
                score=score+(10/recent)
                #score=score+((recent*20)/100)
            #score=score+((recent*50)/100)
        resd[i]=score
    #print(resd)                            
    resd=dict( sorted(resd.items(), key=operator.itemgetter(1),reverse=True))
    return resd
                                        
                                
                            
                            
                    
                    
        

    
            
        
        
            
    
            
            
          
                
        
            
        
        