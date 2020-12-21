#<------- clic sur le play a gauche pour lancer 
# HELLO DOE SCRAPPING 
## HELLO DOE SCRAPPING 
import requests

import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import re
import requests
from itertools import zip_longest
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')


from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
wd.get("https://www.webite-url.com")


### ENTRER L'URL INDEED A SCRAPPER :




#### let do






listTempsPlein=['temps complet','temps plein']
listWordTypeEmploi=["cdi","cdd","auto-entrepreneur","freelance / indépendant"]
listWordJours=["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]  
listFormatHoraires=["de XXhXX à XXhXX","XXh/XXh"]
listFormatVolumeHoraire=["XX heures par semaine","XX heures/semaine","XXh/hebdo","XXh de travail hebdomadaire","XXh/semaine","nombre d'heures : X par semaine","nombre d'heures : XX par semaine","XXh/jour","Xh/jour","Xh/mois","XXh/mois"]
listFormatDureeContrat=['de X à X mois','de X mois'] 
listWordConnecteurs=["au","du"] 
salaryFormat =[['XX,XX € par heure','€/heure'],['XXXXXX € par an','€/an'],['XXXXX € par mois','€/mois'],['XX € par heure','€/heure']]

class Mission:
      def __init__(self,headerJob=0,description=0):
          self.headerJob=headerJob
          self.description=description
          self.jobtitle=self.getJobtitle(headerJob)
          self.companyname=self.getCompanyName(headerJob)
          self.location=self.getLocation(headerJob)
          self.salary=self.getSalary(headerJob)
          self.typeContrat=self.getContratType(description)
          self.horaires=self.gethoraires(description)
          self.workDays=self.getworkingdays(description)
          self.volumeHoraire=self.getvolumehoraires(description)
          self.dureeContrat=self.getDureeContrat(description)

          
      def lookForFormat(self,texte,format):
          formatlist=[]
          listtotale=[]
          for i in range(len(format)):
              if(format[i]=='X'):
                  formatlist.append(0)
              else:
                formatlist.append(1)
          n=0
          verif=1
          indexdeb=0
          while (formatlist[n]==0):
              n=n+1
              
          for j in range(len(texte)):
              verif=1
              if (texte[j]==format[n]):
                  for i in range(n,len(formatlist)):
                    if (formatlist[i]==1 ):
                    # print('lentext'+str(len(texte))+' indice texte= '+str(j+i-n)+' lenformat='+str(len(format))+' indice format='+str(i))
                      if (verif==1 and j+i-n<len(texte) and texte[j+i-n]==format[i]):
                        verif=1

                      else:
                        verif=0;

                  if (verif==1):
                    indexdeb=j
                    list1=[]
                    for a in range(len(formatlist)):
                        if (formatlist[a]==0):
                            list1.append(texte[j+a-n])
                    listtotale.append(list1);
          return listtotale;

      def getconnecteur(self,words,listdaysfound):
          finallist=[]
          for day in range(0,len(listdaysfound)-1):
              index=0
              list1=[]
              for i in range(0,len(words)-1):
                  if (words[i]==listdaysfound[day]):
                    index=i
                    if (words[index+1]=='au'):
                        on=0;
                        list1=[]
                        for j in range(len(listWordJours)):
                            if (listdaysfound[day]==listWordJours[j]):
                              on=1
                            elif (listdaysfound[day+1]==listWordJours[j]):
                              on=2
                            if (on==1):
                              list1.append(listWordJours[j])
                            elif (on==2):
                              list1.append(listWordJours[j])
                              on=3;

              finallist=list1;
          return finallist

      def getJobtitle(self,job):
          a=job.find('a')
          a=a.text
          a=a.replace("\n", "")
          return a  
      def getCompanyName(self,job):
        span=job.find('span', class_='company')
        if (span!=None):
          span=span.text
          span=span.replace("\n","")
          print(span)
          return span
        else:
          return 0 
      def getLocation(self,job):
        span=job.find('span', class_='location')
        if (span!=None):
          return span.text
        else:
            return 0  
      def getSalary(self,job):
          div=job.find('span', class_='salaryText')
          #print(div)
          salary=0;
          if (div!=None):
            for i in range(len(salaryFormat)):
              Xsalary=self.lookForFormat(div.text,salaryFormat[i][0])
              if(len(Xsalary)>0 and salary==0):
                if (i==0):
                  salary = str(Xsalary[0][0])+str(Xsalary[0][1])+','+str(Xsalary[0][2])+str(Xsalary[0][3])
                elif (i==1): 
                  salary = str(Xsalary[0][0])+str(Xsalary[0][1])+str(Xsalary[0][3])+str(Xsalary[0][4])+str(Xsalary[0][5])
                elif (i==2):
                  salary =  str(Xsalary[0][0])+str(Xsalary[0][2])+str(Xsalary[0][3])+str(Xsalary[0][4])
                elif (i==3):
                  salary =  str(Xsalary[0][0])+str(Xsalary[0][1])
                    
                salary=salary+salaryFormat[i][1]
          return salary

  

      def getworkingdays(self,text):
          indexparagraph=0;
          listdaysfound=[];
          words = text.split(' ');
          for day in range(len(listWordJours)):
              n=text.find(listWordJours[day])
              if(n!=-1):
                  listdaysfound.append(listWordJours[day]);
              
              
          listdaysfound=self.getconnecteur(words,listdaysfound);
          if (len(listdaysfound)==0 and self.typeContrat !=0):
            n=self.typeContrat.find('Temps plein')
            if (n!=-1):
              listdaysfound=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
          #print('day found = '+ str(listdaysfound))
          if (len(listdaysfound)==0):
            return 0
          else :
            return listdaysfound; 
      def getContratType(self,text):
            typeContrat='';
            volumeH=[]
            for i in range(len(listWordTypeEmploi)):
                    n = text.find(listWordTypeEmploi[i])
                    if (n==-1):
                      n=-1 
                    else:
                        typeContrat=listWordTypeEmploi[i]
            n = text.find('temps partiel')
            if (n==-1):
                n=-1 
            else:
              typeContrat+=' - Temps partiel'
            for i in listTempsPlein:
              n2 = text.find(i)
              if (n2==-1):
                  n2=-1 
              else:
                if (n!=-1):
                  typeContrat+=' ou Temps plein'
                else :
                    typeContrat+=' - Temps plein'
            if (len(typeContrat)<=1):
              return 0
            else :
                return typeContrat;
      def getvolumehoraires(self,texte):
          volumehoraire='';
          for i in range(len(listFormatVolumeHoraire)):
              list1=[];
              list1=self.lookForFormat(texte,listFormatVolumeHoraire[i]);
              if(len(list1)>0):
                  list1=list1[0]
                  for j in range(len(list1)):
                    volumehoraire+= str(list1[j])
                  if (i<=6):
                    volumehoraire+= 'h/semaine'
                  elif (6<i<=8) :
                    volumehoraire +='h/jour' 
                  elif (8<i<=10)  :
                    volumehoraire +='h/mois'

          for i in listTempsPlein:
            n = texte.find(i)
            if(n!=-1):        
              volumehoraire='35h/semaine'          
          if (len(volumehoraire)<=1):
            return 0
          else :
            return volumehoraire

      def gethoraires(self,texte):
            listhoraires=[]
            horaire=[]
            for i in range(len(listFormatHoraires)):
                list1=[];
                list1=self.lookForFormat(texte,listFormatHoraires[i])
                if(len(list1)>0):
                    for j in range(len(list1)):
                      if (i==0):
                        horaire.append(list1[j][0]+list1[j][1]+'h'+list1[j][2]+list1[j][3]+'-'+list1[j][4]+list1[j][5]+'h'+list1[j][6]+list1[j][7])
                      elif (i==1):
                        horaire.append(list1[j][0]+list1[j][1]+'h/'+list1[j][2]+list1[j][3]+'h')
                      
            #print('horaire='+ str(horaire))
            if (len(horaire)==0):
              return 0
            else :
              return horaire;

      def getDureeContrat(self,text):
            dureeContr=0;
            for i in range(len(listFormatDureeContrat)):
              list1=self.lookForFormat(text,listFormatDureeContrat[i]);
              if(len(list1)>0):
                list1=list1[0]
                if (i==0):
                  dureeContr='de '+str(list1[0])+' à '+str(list1[1])+' mois'
                elif (i==1) :
                  dureeContr=str(list1[0])+' mois'
            return  dureeContr  

      def display(self):
        print('Titre: '+str(self.jobtitle))
        print('Company: '+str(self.companyname))
        print('Lieu: '+str(self.location))
        print('Salaire: '+str(self.salary))
        print('Contrat: '+str(self.typeContrat))
        print('Jour de travail: '+str(self.workDays))
        print('Volume Horaire: '+str(self.volumeHoraire))
        print('Horaires: '+str(self.horaires))
        print('Durée contrat: '+str(self.dureeContrat))

      def displayDescription(self):
        print('Description:'+str(self.description))
      def displayHeaderJob(self): 
          print('Header:'+str(self.headerJob))


def getAllDescription(url):
    reponse=requests.get(url)
    soup= BeautifulSoup(reponse.text,'lxml')
    description=soup.find('div', class_='jobsearch-jobDescriptionText')
    if (description!=None):
      return description.text
    else: 
      return 0 
def lookForFormat(texte,format):
    formatlist=[]
    listtotale=[]
    for i in range(len(format)):
        if(format[i]=='X'):
            formatlist.append(0)
        
        else:
          formatlist.append(1)
        
    
    n=0
    verif=1
    indexdeb=0
    while (formatlist[n]==0):
        n=n+1
        
    for j in range(len(texte)):
        verif=1
        if (texte[j]==format[n]):
            for i in range(n,len(formatlist)):
              if (formatlist[i]==1 ):
               # print('lentext'+str(len(texte))+' indice texte= '+str(j+i-n)+' lenformat='+str(len(format))+' indice format='+str(i))
                if (verif==1 and j+i-n<len(texte) and texte[j+i-n]==format[i]):
                  verif=1

                else:
                  verif=0;

            if (verif==1):
              indexdeb=j
              list1=[]
              for a in range(len(formatlist)):
                  if (formatlist[a]==0):
                      list1.append(texte[j+a-n])
              listtotale.append(list1);
    return listtotale;

def getUrl(url):

    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    driver.get(url)


    summaryItems = driver.find_elements_by_xpath("//a[contains(@class, 'jobtitle turnstileLink')]")
    #jobtitle = driver.find_elements_by_xpath(".//*[contains(@class, 'jobtitle')]")
    #liste=driver.find_elements_by_xpath(".//*[contains(@class, 'row')]")
    job_links = [summaryItem.get_attribute("href") for summaryItem in summaryItems]
    

#def getUrl(url,job):
    #a=job.find('a')
    #link=a['href']
   # linkworking='https://fr.indeed.com/voir-emploi?'+link[7:]
   # return linkworking

def getSalary(job):
          div=job.find('span', class_='salaryText')
          salary=0;
          if (div!=None):
            for i in range(len(salaryFormat)):
              Xsalary=lookForFormat(div.text,salaryFormat[i][0])
              if(len(Xsalary)>0 and salary==0):
                if (i==0):
                  salary = str(Xsalary[0][0])+str(Xsalary[0][1])+','+str(Xsalary[0][2])+str(Xsalary[0][3])
                elif (i==1): 
                  salary = str(Xsalary[0][0])+str(Xsalary[0][1])+str(Xsalary[0][3])+str(Xsalary[0][4])+str(Xsalary[0][5])
                elif (i==2):
                  salary =  str(Xsalary[0][0])+str(Xsalary[0][2])+str(Xsalary[0][3])+str(Xsalary[0][4])
                elif (i==3):
                  salary =  str(Xsalary[0][0])+str(Xsalary[0][1])
                    
                salary=salary+salaryFormat[i][1]
          return salary

def getNewpage(soup):
  ul=soup.find('ul', class_='pagination-list')
  a=ul.findAll('a')
  link='https://www.indeed.fr'+a[-1]['href']
  
  #print(link)
  return link

def getJobtitle(job):
          a=job.find('a')
          a=a.text
          a=a.replace("\n", "")
          return a 

def scrapperJobDescription(url1,n):
    print('in')
    reponse=requests.get(url1)
    ListMission=[]
    listDescription=[]

    listUrl=[]
    listjobs=[]

    if reponse.ok: 
      print('in')
      
      soup= BeautifulSoup(reponse.text,'lxml')
      print(soup)
      listj=soup.findAll('div', class_='result')
      for i in range(len(listj)):
          if (getSalary(listj[i])!=0):
              #print('NEW= salary ='+ str(getSalary(listj[i])+' Titre='+str(getJobtitle(listj[i]))));
              listjobs.append(listj[i])
              listUrl.append(url1)
              

      while (len(listjobs)<n):
        print('in')
        url=getNewpage(soup)
        reponse=requests.get(url)
        if reponse.ok: 
          soup= BeautifulSoup(reponse.text,'lxml')
          listj=soup.findAll('div', class_='result')
          driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
          driver.get(url)
          summaryItems = driver.find_elements_by_xpath("//a[contains(@class, 'jobtitle turnstileLink')]")
          #job_links = [summaryItem.get_attribute("href") for summaryItem in summaryItems]

          for i in range(len(listj)):
            if (getSalary(listj[i])!=0):
              # print('NEW= salary ='+ str(getSalary(listj[i])+' Titre='+str(getJobtitle(listj[i]))));
                listjobs.append(listj[i])
                listUrl.append(summaryItems[i].get_attribute("href"))

          ListMission=[]
          for i in range(len(listjobs)): 
              #print("NEW="+getUrl(listUrl[i],listjobs[i]))
              listDescription.append(getAllDescription(getUrl(listUrl[i],listjobs[i]))) #  DEJA SCRAPPÉ
              listDescription[i]=str(listDescription[i]).lower()
      return listjobs,listDescription



        



def CSVcreation(ListMission):
    from google.colab import drive
    drive.mount('/content/gdrive')
    from os.path import join

    time = datetime.datetime.now()
    date= str(time.day)+'_'+str(time.month)+'_'+str(time.year)+'_'+str(time.minute)
    import os.path
    # Vérifier si le fichier existe ou non

    if os.path.isdir('/content/gdrive/MyDrive/HelloDoeScrapper/'):
        print("Fichier HelloDoeScrapper existant")
    else:
        os.mkdir('/content/gdrive/MyDrive/HelloDoeScrapper/')
        print("Création du fichier hellodoescrapper dans google drive")
    save_path = "/content/gdrive/MyDrive/HelloDoeScrapper/"
    



    entetes = [
        u'Titre',
        u'Companie',
        u'Lieu',
        u'Salaire',
        u'Contrat',
        u'Jour de travail',
        u'Horaires',
        u'Volume Horaire',
        u'Durée contrat',
        u'Description générale',
    ]
    valeurs=[[]]
    for i in range(len(ListMission)):
          job=ListMission[i]
          description=job.description.replace("\n","")

          valeurs.append([str(job.jobtitle),str(job.companyname),str(job.location),
                        str(job.salary),str(job.typeContrat),str(job.workDays),
                        str(job.horaires),str(job.volumeHoraire),str(job.dureeContrat),str(description) ])

    f = open(save_path+'scrapping'+date+'.csv', 'w')
    ligneEntete = ";".join(entetes) + "\n"
    f.write(ligneEntete)
    for valeur in valeurs:
        ligne = ";".join(valeur) + "\n"
        f.write(ligne)

    f.close()
    print('\n Done: tu peux trouver le fichier CSV dans ton drive google @ '+save_path+'scrapping'+date+'.csv')




