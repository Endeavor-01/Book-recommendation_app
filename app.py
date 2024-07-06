from flask import Flask,render_template,request
import pickle
import numpy as np


popular_df= pickle.load(open('popular.pkl', 'rb'))
pt= pickle.load(open('pt.pkl', 'rb'))
books= pickle.load(open('books.pkl', 'rb'))
similarity_scores= pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html',
                            book_name = list(popular_df['Book-Title'].values),
                            author = list(popular_df['Book-Author'].values),
                            image = list(popular_df['Image-URL-M'].values),
                            votes = list(popular_df['num_ratings'].values),
                            # ratings = list(popular_df['avg_ratings'].values),
                            
                            ratings = np.round(popular_df['avg_ratings'].values, 2).tolist()
                            )

@app.route('/recommend')

def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books' , methods=['POST']) 

def recommend_books():
    user_input = request.form.get('user_input')
    # finding index of the movie from pt table
    index = np.where(pt.index == user_input)[0][0]
    # enumerate is done for displaying index as well as item
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data= []

    for i in similar_items:
        item = []
    # [this is for temp_df varaible] here we are storing the entire row of the book-title that we want in temp_df
    # [this is for starting part of the line] here 'books' means the first csv where in that 'books' they are finding the 'title' if it matches pt.index
    #  [this is for last part of the line] here the index[i[0]] means index is where it will display the movie name based on index value[47] 

        temp_df = books[books['Book-Title']== pt.index[i[0]]] 

        # here they are droping the duplicate 'titles'and displaying the entire row of that book by  converting the array in list 
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append (item)
    print(data)    

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')