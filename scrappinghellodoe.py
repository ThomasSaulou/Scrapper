listTempsPlein=['temps complet','temps plein']
listWordTypeEmploi=["cdi","cdd","auto-entrepreneur","freelance / indépendant"]
listWordJours=["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]  
listFormatHoraires=["de XXhXX à XXhXX","XXh/XXh"]
listFormatVolumeHoraire=["XX heures par semaine","XX heures/semaine","XXh/hebdo","XXh de travail hebdomadaire","XXh/semaine","nombre d'heures : X par semaine","nombre d'heures : XX par semaine","XXh/jour","Xh/jour","Xh/mois","XXh/mois"]
listFormatDureeContrat=['de X à X mois','de X mois'] 
listWordConnecteurs=["au","du"] 
salaryFormat =[['XX,XX € par heure','€/heure'],['XXXXXX € par an','€/an'],['XXXXX € par mois','€/mois'],['XX € par heure','€/heure']]



class Mission:
  def __init__(self):
    self.description=0
    self.title=0
    self.company=0
    self.location=0
    self.salary=0
    self.typeContrat=0
    self.horaires=0
    self.workDays=0
    self.volumeHoraire=0
    self.dureeContrat=0
    self.url=0
  def setDescription(self,url):
    driver.get(url)
    self.description = driver.find_elements_by_xpath('//div[contains(@class,"jobDescriptionText")]')[0].text
    self.description = self.description.lower()
    self.description=self.description.replace("\n", " . ")
    #print(description)
  def displayValue(self):
    print(
    #self.description,
    'title=',self.title,'\n',
    'company=',self.company,'\n',
    'location=',self.location,'\n',
    'salary=',self.salary,'\n',
    'typeContrat=',self.typeContrat,'\n',
    'horaires=',self.horaires,'\n',
    'workDays=',self.workDays,'\n',
    'volumeHoraire',self.volumeHoraire,'\n',
    'dureeContrat=',self.dureeContrat,'\n',
    'url=',self.url)



  def lookForFormat(self,text,format):
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
          
      for j in range(len(text)):
          verif=1
          if (text[j]==format[n]):
              for i in range(n,len(formatlist)):
                if (formatlist[i]==1 ):
                # print('lentext'+str(len(text))+' indice texte= '+str(j+i-n)+' lenformat='+str(len(format))+' indice format='+str(i))
                  if (verif==1 and j+i-n<len(text) and text[j+i-n]==format[i]):
                    verif=1

                  else:
                    verif=0;

              if (verif==1):
                indexdeb=j
                list1=[]
                for a in range(len(formatlist)):
                    if (formatlist[a]==0):
                        list1.append(text[j+a-n])
                listtotale.append(list1)
      return listtotale

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
  def getvolumehoraires(self,text):
    volumehoraire='';
    for i in range(len(listFormatVolumeHoraire)):
        list1=[];
        list1=self.lookForFormat(text,listFormatVolumeHoraire[i]);
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
      n = text.find(i)
      if(n!=-1):        
        volumehoraire='35h/semaine'          
    if (len(volumehoraire)<=1):
      return 0
    else :
      return volumehoraire

  def gethoraires(self,text):
      listhoraires=[]
      horaire=[]
      for i in range(len(listFormatHoraires)):
          list1=[];
          list1=self.lookForFormat(text,listFormatHoraires[i])
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

  def setdescriptioninfo(self,text):



    self.dureeContrat=self.getDureeContrat(text)
    self.horaires=self.gethoraires(text)
    self.volumeHoraire=self.getvolumehoraires(text)
    self.typeContrat=self.getContratType(text)
    self.workDays=self.getworkingdays(text)


def scrap(url,nbMission):
  a=0
  b=0
  listMission=[]
 
  n=0
  while n<nbMission  :


    link=url
    link+='&start='+str(a*10)
    driver.get(link)
    a+=1
    
    
    job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

    for job in job_card:

            b+=1
            #print(job.text)
          # print('\n \n')

        #.   not all positions have salary
            try:
                
                salary = job.find_element_by_xpath('.//span[@class="salaryText"]').text
            except:
                salary = "None"
            

            if salary !="None": 
                
                mission=Mission()  
                n+=1
                #.  tells only to look at the element  
                mission.salary=salary     

            #.  not all companies have review
                #try:
                #    review = job.find_element_by_xpath('.//span[@class="ratingsContent"]').text
                #except:
                #    review = "None"
                #reviews.append(review)

                try:
                    location = job.find_element_by_xpath('.//span[contains(@class,"location")]').text
                except:
                    location = "None"
            #.  tells only to look at the element       

                mission.location=location
                
                try:
                    title  = job.find_element_by_xpath('.//h2[@class="title"]//a').text
                except:
                    title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
      
                mission.title=title
                link=job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")

                
                companie=job.find_element_by_xpath('.//span[@class="company"]').text
              
                mission.company=companie
                mission.url=link
                
                listMission.append(mission)
                #driver.get(link)
    
    for mission in listMission:
      
      mission.setDescription(mission.url)
      mission.setdescriptioninfo(i.description)     
    return listMission


def CSVcreation(ListMission):
    from google.colab import drive
    drive.mount('/content/gdrive')
    from os.path import join
    import datetime

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
          description=job.description

          valeurs.append([str(job.title),str(job.company),str(job.location),
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

