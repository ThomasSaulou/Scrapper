#<------- clic sur le play a gauche pour lancer 
# HELLO DOE SCRAPPING 
## HELLO DOE SCRAPPING 
#!pip install selenium
#!apt-get update # to update ubuntu to correctly run apt install
#!apt install chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin

import requests

import datetime

from bs4 import BeautifulSoup
#from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import re
import requests
from itertools import zip_longest
#from webdriver_manager.chrome import ChromeDriverManager
import sys
#sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')






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

semantique = {'heure':['heure','XXhXX','XXh','Xh','XX heures','X:XX','XX:XX'],
              'jour':["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"],
              'argent':['€','euros','euro'],
              'periode':['jour','jours','semaine','semaines','mois','années','année','hebdo','hebdomadaire']
              }
              
            

Category = {'Accueil Visiteurs': ["hôtesse","hôte","hôte d'accueil","hôtesse d'accueil","guichetier","secrétaire hôte","standardiste","agent d'accueil","receptionniste","hôte(sse) d'accueil","hote(sse) d'accueil"], 
        'Service': ["serveur","serveur polyvalent","employé de restauration","employé de restauration rapide","employé polyvalent en restauration","barista","barman","barmaid","serveuse","limonadier","équipier polyvalent restauration rapide","équipier polyvalent restauration","garçon limonadier","extra en restauration","serveur en salle"], 
        'Billeterie':[],
        "Contrôle d'accès":[],
        "Tenue de Vestiaire":["vestiaire"],
        "Voiturier":["voiturier","chasseur bagagiste","bagagiste"],
        "Accueil Hôtellerie":["veilleur de nuit","veilleuse de nuit","gardien veilleur","receptionniste","surveillant de nuit"],
        "Street Marketing":["distributeur d'imprimés publicitaires","distributeur/trice d'imprimés publicitaires","distributeur de prospectus","distributeur de journaux","distribution boites aux lettres","distributeur de presse","distributeur de presse gratuite","distributeur de flyers","distributeur de flyer","distribution de flyers"],
        "Animation / Démonstration":["animateur commercial","animateur street marketing"],
        "Baby-sitting":["babysitter","baby-sitter","garde d'enfant","garde d'enfants","garde d'enfant à domicile","babysitting","baby-sitting","sortie d'ecole","sortie d'école","garde d’enfant"],
        "Inventaire":["inventoriste","équipier en inventaire","auditeur en inventaire"],
        "Déménagement":["déménageur"],
        "Manutention":["manutentionnaires","manutentionnaire","manutention","employé logistique","équipier logistique","agent logistique"],
        "Conditionnement":["préparateur de commandes","préparateur de commande","magasinier","logisticien","conditionneur","agent de conditionnement","préparateur de paniers","équipier logistique"],
        "Petites Mains":[],
        "Employé agricole":["vendanges","cueillleur","cueilleuse"],
        "Etiquetage / Stock":["magasinier","stockiste","reserviste"],
        "Vente en Boutique":["vendeur","vendeur polyvalent","conseiller de vente"],
        "Vente Luxe":[],
        "Libre Service & Merchandizing":["libre-service","rayonniste","employé de rayon","vendeur rayon","vendeur polyvalent","employé libre service","employé de mise en rayon","équipier mise en rayon"],
        "Caisse & Enlèvement":["caissier polyvalent","vendeur caissier","hôte de caisse","hôtesse de caisse","caissier","agent caisse","employé commercial caisse","hôte(sse) de caisse","hote(sse) de caisse"],
        "Prospection Commerciale":[],
        "Support Client":["téléconseiller","support client","SAV","Service Après Vente","hôte relation client","helpdesk","help desk"],
        "Saisie de Données":["secrétaire administratif","assistant administratif","opérateur de saisie","saisie de données"],
        "Aide Admin":[],
        "Recherche en Ligne":[],
        "Recruteur de Donateurs":["recruteur de donateurs","recruteur de donateur"],
        "Livraison":["livreur","coursier","Livreur/livreuse"],
        "Plongeur":["plongeur","plongeuse"],
        "Restauration Rapide":["équipier","employé de restauration rapide","employé polyvalent de restauration","employé polyvalent en restauration"]} 
        
class Mission:
      def __init__(self):
          self.description='None'
          self.title='None'
          self.company='None'
          self.location='None'
          self.salary='None'
          self.typeContrat='None'
          self.horaires='None'
          self.workDays='None'
          self.volumeHoraire='None'
          self.dureeContrat='None'

          
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
                        typeContrat+=' ' + listWordTypeEmploi[i]
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
        print('Titre: '+str(self.title))
        print('Company: '+str(self.company))
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
      def setdescriptioninfo(self,text):
        self.dureeContrat=self.getDureeContrat(text)
        self.horaires=self.gethoraires(text)
        self.volumeHoraire=self.getvolumehoraires(text)
        self.typeContrat=self.getContratType(text)
        self.workDays=self.getworkingdays(text)    


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


def updateMission(mission):
    mission.title=categoriseTitle(mission.title)
    return mission

def categoriseTitle(title):
  newtitle='None'
  title=title.lower()
  for titre in Category:
    for i in Category[titre]: 
      n=title.find(i)
     # print(n)
      if n!=-1:
        newtitle=titre
  if  newtitle=='None' :
    return title
  else :       
    return newtitle
    
        
def CSVcreation(df,file):
    from google.colab import drive
    drive.mount('/content/gdrive')
    from os.path import join

    time = datetime.datetime.now()
    date= str(time.day)+'_'+str(time.month)+'_'+str(time.year)+'_'+str(time.hour+1)+'_'+str(time.minute)
    import os.path
    # Vérifier si le fichier existe ou non
    save_path = '/content/gdrive/MyDrive/'+file+'/'
    if os.path.isdir(save_path):
        print("Fichier HelloDoeScrapper existant")
    else:
        os.mkdir(save_path)
        print("Création du fichier hellodoescrapper dans google drive")
    
    df.to_csv(save_path+'scrapping'+date+'.csv')
    print('\n Done: tu peux trouver le fichier CSV dans ton drive google @ '+save_path+'scrapping'+date+'.csv')

def scrap(driver,url,nbmin):
    options = webdriver.ChromeOptions()
    df = pd.DataFrame(columns=["Title","Location","Company","Salary","URL"])
    i=0
    n=0
    while n<nbmin:
      driver.get(url+'&start='+str(i))
      i+=10
      jobs = []
      driver.implicitly_wait(4)
      

      for job in driver.find_elements_by_class_name('result'):

        soup = BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
        
        try:
          title = soup.find("a",class_="jobtitle").text.replace("\n","").strip()
          
        except:
          title = 'None'

        try:
          location = soup.find(class_="location").text
        except:
          location = 'None'

        try:
          company = soup.find(class_="company").text.replace("\n","").strip()
        except:
          company = 'None'

        try:
          salary = soup.find(class_="salary").text.replace("\n","").strip()
        except:
          salary = 'None'
          
        try:
          job_url=job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
        except:
          job_url='None' 
        if salary!='None':   
          df = df.append({'Title':title,'Location':location,"Company":company,"Salary":salary,"URL":job_url},ignore_index=True)
          n+=1
          print("Got these many results:",n)
    return df

def getDescription(driver,URLs,df):
    df['Description']='None'
    for i in range(len(URLs)):
      driver.get(URLs[i])
      description=driver.find_elements_by_xpath('//div[contains(@class,"jobDescriptionText")]')[0].text
      description=description.lower()
      description=description.replace("\n", " . ")
      df['Description'][i]=description
    return df

def switchURLDesc(df):
  col_list = list(df)
  col_list[4], col_list[5],col_list[6], col_list[7], col_list[8], col_list[9], col_list[10] = col_list[6], col_list[7], col_list[8], col_list[9], col_list[10],col_list[5], col_list[4]
  df.columns = col_list
  return df



def updateTable(ListMission,df):
  for i in range(len(ListMission)):
    mission=ListMission[i]
    mission=updateMission(mission)
    df['Description'][i]=mission.description
    df['Title'][i]=mission.title
    df['Location'][i]=mission.location
    df['Company'][i]=mission.company
    df['URL'][i]=mission.url
    df['TypeContrat'][i]=mission.typeContrat
    df['Horaires'][i]=mission.horaires
    df['WorkDays'][i]=mission.workDays
    df['VolumeHoraire'][i]=mission.volumeHoraire
    df['dureeContrat'][i]=mission.dureeContrat
  return df 

def scraphellodoe(driver,url,nbmin):
  df=scrap(driver,url,nbmin)
  df=getDescription(driver,df.URL,df)
  df['TypeContrat']='None'
  df['Horaires']='None'
  df['WorkDays']='None'
  df['VolumeHoraire']='None'
  df['dureeContrat']='None'

  ListMission=[]
  for i in range(len(df)):
    mission=Mission()
    mission.title=df.iloc[i]['Title']
    mission.location=df.iloc[i]['Location']
    mission.company=df.iloc[i]['Company']
    mission.url=df.iloc[i]['URL']
    mission.description=df.iloc[i]['Description']
    mission.setdescriptioninfo(mission.description)
    ListMission.append(mission)
  df=switchURLDesc(df) 
  df=updateTable(ListMission,df) 
  return df
    

import re
semantique = {'heure':['heure','\d\dh\d\d',"\d\dh",'\dh','\d\d heures','\d:\d\d','\d\d:\d\d','/heure','midi','minuit'],
              'jour':["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche","lundis","mardis","mercredis","jeudis","vendredis","samedis","dimanches","-dimanche"],
              'argent':['€','euros','euro '],
              'periode':['jour','jours','semaine','semaines','mois','années','année','hebdo','hebdomadaire','/s'],
              'link':['de','-','à',"jusqu'à",'au','a'],
              'ou':['ou'],
              #'flexible':['flexible'],
              'flexible':["payé à l’heure","autant que vous voulez",'flexible','flexibles','en fonction de vos disponibilités','adaptables'],
              'horaires':['horaires:'],
              'NOK':['contacter'],
              'durée':['durée du contrat :']
             # 'sortie école':["sortie d’école"],
             
              }




def findstrict(word,val):
  if word.startswith(val):
    if  word.endswith(val):
      return True
  return False
  

class TexteAnalyse:
      def __init__(self,description):
        self.description=description
        self.listsentence=[]
        for i in range(len(description)):
          if description[i]=="." and i<len(description)-1:
            if description[i-1].isnumeric() and description[i+1].isnumeric(): 
              s=list(description)
              s[i]=','
              description="".join(s)
        listsent=description.split(".")
        for i in listsent:
          self.listsentence.append(phrase(i))
      def displayDescription(self):
        print(self.description)
      def displaySentencelabel(self):
        for i in self.listsentence:
          i.displaylabel()
      def displayInterpret(self):
        for i in self.listsentence:  
          i.displayInterpretation() 
      def getHoraire(self):
        listhoraire=[]
        for i in self.listsentence :
          ok=True
   
          listinterpret=i.listinterpret
          for interpret in listinterpret:
            
            if interpret.meaning=='NOK':
              ok=False
          if ok:    
            for interpret in listinterpret:
              
              if interpret.meaning=='sortie ecole':
                listhoraire.append('sortie école')
              if interpret.meaning=='plageHoraire':
                for word in interpret.listWords:
                  
                    if word.label[0]=='jour' or word.label[0]=='heure' or word.label=='heure':
                      listhoraire.append(word.word)
                   
        return listhoraire




      def getVolumeHoraire(self): 
        listVolume=[]
        for i in self.listsentence :

          listinterpret=i.listinterpret
          for interpret in listinterpret:

            if interpret.meaning=='volumeHoraire':

              for word in interpret.listWords:
   
                  if word.label[0]=='heure':
          
                    listVolume.append(word.word)
                  
        return listVolume        
      def getFlexible(self): 
        for i in self.listsentence :
    
          listinterpret=i.listinterpret
          for interpret in listinterpret:
            if interpret.meaning=='flexible':
              return True 
        return False    
      def getWorkdays(self):
        listDays=[]
        for i in self.listsentence :
          
          listinterpret=i.listinterpret
          for interpret in listinterpret:
            
            if interpret.meaning=='WorkDays':
              for word in interpret.listWords:                  
                  if word.label[0]=='jour':
                    listDays.append(word.word)
        return listDays 
        

       
              
        
class phrase:
      def __init__(self,sentence):
        self.sentence=sentence
        self.listword=sentence.split(" ")
        self.listwordlabel=[]
        for i in self.listword:
          self.listwordlabel.append(word(i))
        self.listinterpret=self.interpretationSentence()  
      def displaySentence(self):
          print(self.sentence) 
      def displaylabel(self):
          listdisp=''
          for i in self.listwordlabel:
            w,l=i.getwordlabel()
            listdisp+=' '+w
            if len(l)!=0:
          
              listdisp+=' (='
              for i in l:
                listdisp+=i+','
              listdisp+=' )'  
          print(listdisp)
      def displayInterpretation(self):
        self.displaylabel() 
        for i in self.listinterpret:
          i.displayinterpret()
      def interpretationSentence(self):
        listlab=[]
        listinterpret=[]
        listindexmot=[]
        for i in semantique['flexible']:
          n=self.sentence.find(i)
          if n!=-1:
            meaning=interpret('flexible')
            listinterpret.append(meaning)



        
        for j in range(len(self.listwordlabel)):
          wordz=self.listwordlabel[j]
          for i in range(len(wordz.label)):
            listindexmot.append(j)
          
            listlab.append(wordz.label[i]) 
        
        for i in range(len(listlab)):
          if i<len(listlab)-2 and listlab[i]=='jour' and listlab[i+1]=='link' and listlab[i+2]=='jour':
              
              meaning=interpret('WorkDays')
              a=0
              for jour in semantique['jour']:
                
                if jour==self.listwordlabel[listindexmot[i]].word :
                  a=1
                  meaning.listIndex.append(listindexmot[i])
                 
                  wo=word(jour)
                  wo.label=['jour']
                  meaning.listWords.append(wo)

                elif  jour==self.listwordlabel[listindexmot[i]+2].word:
                  a=2
                  meaning.listIndex.append(listindexmot[i+1])
                  wo=word(jour)
                  wo.label=['jour']
                  meaning.listWords.append(wo)
                  
                elif a==1:
                  meaning.listIndex.append(listindexmot[i+1])
                  wo=word(jour)
                  wo.label=['jour']
                  meaning.listWords.append(wo)
                 
              listinterpret.append(meaning)   
          elif   listlab[i]=='jour':
              meaning=interpret('WorkDays')
              meaning.listIndex.append(listindexmot[i])
              meaning.listWords.append(self.listwordlabel[listindexmot[i]])
              listinterpret.append(meaning)

          if listlab[i]=='NOK':
            meaning=interpret('NOK')
            meaning.listIndex.append(listindexmot[i])
            meaning.listWords.append(self.listwordlabel[listindexmot[i]])
            listinterpret.append(meaning)
          if i<len(listlab)-1 and listlab[i]=='argent' and listlab[i+1]=='heure':
           
            meaning=interpret('salaire')
            meaning.listIndex.append(listindexmot[i])
            meaning.listIndex.append(listindexmot[i+1])
            meaning.listWords.append(self.listwordlabel[listindexmot[i]])
            meaning.listWords.append(self.listwordlabel[listindexmot[i+1]])
            listinterpret.append(meaning)
          if i<len(listlab)-1 and listlab[i]=='heure' and listlab[i+1]=='periode':
            meaning=interpret('volumeHoraire')  
            if listlab[i-1]=='ou' :
              meaning.listIndex.append(listindexmot[i-2])
              meaning.listWords.append(self.listwordlabel[listindexmot[i-2]])

            
            meaning.listIndex.append(listindexmot[i])
            meaning.listIndex.append(listindexmot[i+1])
            meaning.listWords.append(self.listwordlabel[listindexmot[i]])
            meaning.listWords.append(self.listwordlabel[listindexmot[i+1]])
            listinterpret.append(meaning)
  
          if i<len(listlab)-2 and listlab[i]=='heure' and  listlab[i+1]=='link'  and listlab[i+2]=='heure' :
              meaning=interpret('plageHoraire')
              if listlab[i-1]=='jour' or listlab[i-2]=='jour':
              

                meaning.listIndex.append(listindexmot[i-1])
                meaning.listWords.append(self.listwordlabel[listindexmot[i-1]])
              meaning.listIndex.append(listindexmot[i])
              meaning.listWords.append(self.listwordlabel[listindexmot[i]])
              meaning.listIndex.append(listindexmot[i+2])
              meaning.listWords.append(self.listwordlabel[listindexmot[i+2]])
              listinterpret.append(meaning)


              


          if listlab[i]=='horaires':
            meaning=interpret('plageHoraire')
            for j in range(2,len(self.listword)):
              self.listwordlabel[j].label='heure'
            
              meaning.listIndex.append(j)
              meaning.listWords.append(self.listwordlabel[j])
              listinterpret.append(meaning)
   
          
        return listinterpret


class interpret:
    def __init__(self,meaning):
        self.listIndex=[]
        self.listWords=[]
        self.meaning=meaning
    def displayinterpret(self):
      #for i in self.listIndex:
        #print(i)
      for i in self.listWords:
        wordlabel=i.getwordlabel()
        print(wordlabel[0],wordlabel[1])
      print(self.meaning)


class word:
  def __init__(self,word):
    self.word=word
    self.label=[]
    self.labelised(word)
    
  def labelised(self,word):
    previous=''
    for i in semantique:
      for j in semantique[i]:
        x=re.findall('^'+j+'$',self.word)
        if len(x)!=0:
          if previous!=i:
            self.label.append(i)
            previous=i    
  def getwordlabel(self):
        return self.word,self.label  


def affinage(df):
  for i in range(len(df)):
    title=df.iloc[i]['Title'].lower()
    description=title+'. '
    description+=str(df.iloc[i]['Description'])
    texte=TexteAnalyse(description)
    flex=texte.getFlexible()
    df['Horaires'][i]=texte.getHoraire()
    df['VolumeHoraire'][i]=texte.getVolumeHoraire()
    df['WorkDays'][i]=texte.getWorkdays()
    n=description.find("sortie d’école")
    if n!=-1:
      df['Horaires'][i]="Flexible"
      df['WorkDays'][i]=["lundi",'mardi','mercredi','jeudi','vendredi']
      df['VolumeHoraire'][i]="variable"
      df['dureeContrat'][i]="Flexible"
    if flex:
      df['Horaires'][i]="Flexible"
      df['WorkDays'][i]="Flexible"
      df['VolumeHoraire'][i]="À la carte"
      df['dureeContrat'][i]="Flexible"
  return df 
def cleaning(df):
    for i in range(len(df)):
        horaire=df.iloc[i]['Horaires']
        workdays=df.iloc[i]['WorkDays']
        listday=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
        listhoraire=[]
        listworkdays=[]
        if workdays!='Flexible':
           for j in workdays:
                for day in listday:
                  if j==day or j==day+'s':
                    if day not in listworkdays:
                     listworkdays.append(day)
           df['WorkDays'][i]= listworkdays
        if horaire!='Flexible':
          for j in horaire:
            if j not in listhoraire and j!='et' and j!='le' and j!='':
              listhoraire.append(j)
          df['Horaires'][i]= listhoraire
    return df



