from utilml import listofcleanfromdir 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from PIL import Image
import numpy as np

unique = 'f004c39664dd4031b403c803400b0f59'

def transform_format(val):
    '''
    mask transformation
    '''
    if val == 0:
        return 255
    else:
        return val

def generatewordcloud(unique):
    '''
    generates wordcloud for website
    '''
    #достанем весь текст
    flat_str = ''.join(''.join(sub) for sub in listofcleanfromdir(unique))
    #кол-во слов
    #print(len(flat_str.split()))
    #возьмем маску
    mask = np.array(Image.open("files/blue.png"))



    #transformed_mask = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)
    #for i in range(len(mask)):
    #    transformed_mask[i] = list(map(transform_format, mask[i]))


    wordcloud = WordCloud(background_color="white",max_font_size=100, mask=mask).generate(flat_str)
    image_colors = ImageColorGenerator(mask)

    wordcloud.recolor(color_func=image_colors)

    wordcloud.to_file("static/"+unique+".png")
    

generatewordcloud(unique)  
