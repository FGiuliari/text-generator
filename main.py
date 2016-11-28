from crawler import crawler
import markovify

c=crawler()
if True==False :
    t1=""
    for i in range(1,42):
        t1+=c.getStory("s/2636963/"+str(i))

    t2=""    
    for i in range(1,23):
        t2+=c.getStory("s/5302762/"+str(i))

    t3=""
    for i in range(1,24):
        t3+=c.getStory("s/7075713/"+str(i))
        

    text_model1 = markovify.Text(t1,state_size=3)
    text_model2 = markovify.Text(t2,state_size=3)
    text_model3 = markovify.Text(t3,state_size=3)

    model_combo = markovify.combine([text_model1,text_model2,text_model3])

        
    text2=open("C:/Users/artix/Desktop/Nuovacartella/harry potter markov/new.txt","w") 

    # Build the model.

    # Print five randomly-generated sentences
    for i in range(1000):
        text2.write(model_combo.make_sentence(tries=1000)+"\n")

    text2.close()
    print("wee")
