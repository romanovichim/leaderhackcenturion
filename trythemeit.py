import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    import numpy as np
    import pandas as pd
    from nltk.corpus import stopwords
    import nltk
    from sklearn.model_selection import GridSearchCV
    from scipy.spatial.distance import cosine
    from statistics import median
  
#выполнить
#nltk.download()
#article
#https://towardsdatascience.com/nlp-for-topic-modeling-summarization-of-legal-documents-8c89393b1534

#take list of documents

#Вессель Нишце
unique = 'f004c39664dd4031b403c803400b0f59'

#корпоративный пример
uniquek = '247a47f3e28a4e189af5d95f6bda2dec'
from utilml import listofcleanfromdir  
from utilml import listofsentences   

#print(generatelistfromdir())


# Python program to get average of a list 
def average(lst): 
    return sum(lst) / len(lst) 

def column(matrix, i):
    '''
    returns column of darray 0,1,2,3....
    '''
    return [row[i] for row in matrix]



# Show top n keywords for each topic
def show_topics(vectorizer, lda_model, n_words=20):
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))

    return topic_keywords


#lexsort of array
def tiensort(Outputl):
    forsort=np.array(Outputl)
    forsort[np.lexsort((forsort[:, 2], forsort[:, 1]))]

    return forsort

def gridsearch(data_vectorized):
    '''
    data_vectorized - data after fit_transform CountVectorizer
    return best parameters топики и
    '''
    # Define Search Param
    search_params = {'n_components': [5,7,9,10], 'learning_decay': [.3,.5, .7, .9]}

    # Init the Model
    lda = LatentDirichletAllocation()

    # Init Grid Search Class
    model = GridSearchCV(lda, param_grid=search_params)

    # Do the Grid Search
    model.fit(data_vectorized)
    
    # Best Model
    best_lda_model = model.best_estimator_

    # Model Parameters
    #print("Best Model's Params: ", model.best_params_)
    return best_lda_model




def generatetopics(unique):
    '''
    unique - for path
    script make topic sentences from documents
    '''
    work   =  listofcleanfromdir(unique)

    sentlist = listofsentences(unique)


    vect = CountVectorizer(ngram_range=(1,1),stop_words = stopwords.words())

    

    dtm = vect.fit_transform(work)
    #подбор параметров
    best_lda_model=gridsearch(dtm)
    
    lda_dtf=best_lda_model.fit_transform(dtm)



    #посчитаем коэффиценты 
    
    keywords = np.array(vect.get_feature_names())
    final_arr = []
    #ids_arr = []
    warr=[]
    #Тематичность и Информативность
    for topic in best_lda_model.components_:
        Outputl=[]
        #для хранения весов
        
        for sentence in work:
            #cчитам тематичность каждого предложения
            templ = []
            iems = 0
            tprofile=[]
            #слепливаем два массива
            for k,wprob in zip(keywords,topic):                       
                    #слово и его пробабилити    
                    #print(k,wprob)
                    swords = sentence.split()
                    
                    for w in swords:
                        if(w == k):
                            #слов меньше тк убраны мальенькие - меньше 3
                            # считаем тематичность
                            iems = iems + wprob

                    #считаем тематический профиль предложения
                    if(k in swords):
                        tprofile.append(wprob)
                    else:
                        tprofile.append(0)

                    
        
            
            #считаем тематический профиль cosine distance between sentence and topic
            tems= cosine(tprofile,topic) 
            if(np.isnan(tems)==True):
                tems=0
            templ.append(sentence)
            #iems - посчитанная информативность
            #tems - посчитанная тематичность
            templ.append(iems)
            templ.append(tems)
            Outputl.append(templ)


        #print(Outputl)
        #возьмем пока что медианные пороги пороги
        #Здесь надо подругому но пока так будем брать

            
        iemsporog = median(column(Outputl,1))
        aiemsporog = average(column(Outputl,1))
        #print(aiemsporog)
        temsporog = median(column(Outputl,2))
        atemsporog = average(column(Outputl,2))
        #print(int(round(aiemsporog*atemsporog)))


        #ВЕС тематическо информативный
        weight = int(round(aiemsporog*atemsporog))
        #print("вес",weight)
        #ограничитель
        
        if(weight > 10):
            weight = 10
        if(weight < 4):
            weight = 4
        
        warr.append(weight)
        #print('----')
        #for row in Outputl:
        #    print(row)
        
        #print(iemsporog,temsporog)


        #отсортируем по тематичности и информатичности
        #Outputsort= tiensort(Outputl[:20])
        '''
        itoglist=[]
        i=0
        #сюда будем собирать итоговые предложения
        #делая доп очистку
        for row in Outputl:
            if(row[0]!=''):
                #print(row)
                itoglist.append(sentlist[i])

            i = i+1 

        #print('----')


        final_arr.append(itoglist)
        '''
        

        '''
        itoglist=[]
        i=0
        for row in Outputl:
            #print(i,row)
            if(row[1] > iemsporog and row[2] > temsporog):
                itoglist.append(sentlist[i])
                
            i = i+1 

        #берем по id из не очищенных предложений
        final_arr.append(itoglist)
        '''
    
    #print(warr)
    
    #конец расчета коэффицентов 
    final_arr = []

    #сколько тем
    n_comp=0
    for topic in best_lda_model.components_:
        n_comp=n_comp+ 1



    # аргсорт предложений относительно вероятности слова по теме    
    for i in range(n_comp):
        topic=np.argsort(lda_dtf[:,i])[::-1]
        temparr=[]
        weightitog= warr[i]
        for i in topic[:weightitog]:
            temparr.append(".".join(sentlist[i].split(".")[:2]))

        #print(len(temparr))
        final_arr.append(temparr)

    
    
    
    #print(final_arr)
    return final_arr
   
 

    


    '''
    topic_keywords = show_topics(vectorizer=vect, lda_model=best_lda_model, n_words=15) 
    
    # Topic - Keywords Dataframe
    df_topic_keywords = pd.DataFrame(topic_keywords)
    df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
    df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df_topic_keywords.head())
    ''' 
    
    ''' 
    lda=LatentDirichletAllocation(n_components=5)
    lda_dtf=lda.fit_transform(dtm)


    sorting=np.argsort(lda.components_)[:,::-1]
    features=np.array(vect.get_feature_names())



    #достанем
    #import mglearn
    #mglearn.tools.print_topics(topics=range(5), feature_names=features, sorting=sorting, topics_per_chunk=5, n_words=10)

    #объединим все тексты в один


    final_arr = []

    for i in range(5):
        topic=np.argsort(lda_dtf[:,i])[::-1]
        temparr=[]
        for i in topic[:10]:
            temparr.append(".".join(sentlist[i].split(".")[:2]))

        final_arr.append(temparr)


    return  final_arr
    '''
    
#generatetopics(uniquek)

#print()
for i in generatetopics(uniquek):
    print("topiccccccccccc")
    print(i)



















        
    


    
