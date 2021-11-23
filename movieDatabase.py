#create database in python 
#make all the  input fields and the labels for the inputting 
#make submission button
#make a submitting function

from tkinter import * 
import sqlite3

root = Tk()
root.title('Movie database')
root.geometry('600x600')

#make functions
def submit():
    if e_movie_name.get() == '':
        print('Fill all the fields')
    else: 
        #need to open the database within the function
        movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db')
        cursor = movieDat.cursor()
        #insert into table
        cursor.execute( 'insert into movie_ratings values (:movie_name,:movie_year,:favourite_actor,:score)',
        {
            'movie_name':e_movie_name.get(),
            'movie_year':e_movie_year.get(),
            'favourite_actor':e_favourite_actor.get(),
            'score':e_score.get()
        }
        )
        print('added') #test
        movieDat.commit() #commit changes
        movieDat.close() #close the connection
        #clear fields
        e_movie_name.delete(0,END)
        e_movie_year.delete(0,END)
        e_favourite_actor.delete(0,END)
        e_score.delete(0,END)

def show_all():
    #as always need a cursor inside the function to interact wt database
    movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db')
    cursor = movieDat.cursor()
    root.geometry('800x600')

    #show all results + oid
    cursor.execute('select *,oid from movie_ratings')
    records = cursor.fetchall()
    print_records = ''
    for row in records:
        print_records+=str(row)+'\n'
    global show_all_label 
    show_all_title = Label(results_frame,text = 'All results:',fg = 'purple',pady=10)
    show_all_title.grid(row = 0,column=0)
    show_all_label = Label(results_frame, text = print_records,pady=10)
    show_all_label.grid(row = 1,column=0)
    

    movieDat.commit()
    movieDat.close()

def showSingleResult(provided_oid): 
    #create connection to dat 
    movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db')
    cursor = movieDat.cursor()
    root.geometry('800x600')
    #select one result based on oid
    cursor.execute("select *,oid from movie_ratings where oid ==%s"%int((provided_oid)))
    singleRecord = cursor.fetchone()
    print(singleRecord)
    print_record = ''
    for i in singleRecord:
        print_record += str(i) + ' '
    show_all_title = Label(results_frame,text = 'All results:',fg = 'purple',pady=10)
    show_all_title.grid(row = 0,column=0)
    show_all_label = Label(results_frame, text = 'Record '+str(singleRecord[len(singleRecord)-1])+':\n ' +print_record,pady=30,padx=20)
    show_all_label.grid(row = 1,column=0)

    movieDat.commit()
    movieDat.close()
    e_show_oid.delete(0,END)

def deleteSingleResult(provided_oid):
    #connection ad cursor
    movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db')
    cursor = movieDat.cursor()
    cursor.execute('delete from movie_ratings where oid ==%s'%int((provided_oid)))

    movieDat.commit()
    movieDat.close()
    e_del_oid.delete(0,END)
#update entry
def saveUpdate():
    record_id = e_update_record.get()
    movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db')
    cursor = movieDat.cursor()
    cursor.execute(""" 
    update movie_ratings set 
    movie_name = :name,
    movie_year = :year,
    favourite_actor = :actor,
    score = :score
    where oid ==:oid
    """,
    {
        'name':e_movie_name.get(),
        'year':e_movie_year.get(),
        'actor':e_favourite_actor.get(),
        'score':e_score.get(),
        'oid':record_id

    }
    )

    movieDat.commit()
    movieDat.close()
    e_update_record.delete(0,END)
    new.destroy()

#update record 
def updateRecord(provided_oid):
    global new
    #make a new window with all the fields t update
    new = Tk()
    new.title('Movie database')
    new.geometry('400x400')

    entry_frame = LabelFrame(new,padx=10,pady=10)
    entry_frame.grid(row=1,column=0,columnspan=2)
    movie_name = Label(entry_frame, text = 'Movie name')
    movie_name.grid(row = 1,column=0)
    movie_year = Label(entry_frame, text = 'Movie year')
    movie_year.grid(row = 2,column=0)
    favourite_actor = Label(entry_frame, text = 'Favourite actor')
    favourite_actor.grid(row = 3,column=0)
    score = Label(entry_frame, text = 'score')
    score.grid(row = 4,column=0)

    #declare global variables
    global e_movie_name
    global e_movie_year
    global e_favourite_actor
    global e_score

    #entry fields
    e_movie_name = Entry(entry_frame,width=30)
    e_movie_name.grid(row = 1, column=1)
    e_movie_year = Entry(entry_frame,width=30)
    e_movie_year.grid(row = 2, column=1)
    e_favourite_actor = Entry(entry_frame,width=30)
    e_favourite_actor.grid(row = 3, column=1)
    e_score = Entry(entry_frame,width=30)
    e_score.grid(row = 4, column=1)

    #pull info out of the database to insert it 
    movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db') #dasves database in the directory im in 
    cursor = movieDat.cursor()
    cursor.execute('select * from movie_ratings where oid ==%s'%(provided_oid))
    records = cursor.fetchall()
    #assign results to existing fields 
    for record in records:
        e_movie_name.insert(0,record[0]) #assign existing values
        e_movie_year.insert(0,record[1])
        e_favourite_actor.insert(0,record[2])
        e_score.insert(0,record[3])

    # create a save button
    save_btn = Button(entry_frame,text = 'Update record',command= saveUpdate)
    save_btn.grid(row = 5,column=0,columnspan=2)
    movieDat.commit() #commit changes
    movieDat.close()    

#create a database 
movieDat = sqlite3.connect('/Users/helena_adamkova/Documents/Just IT/projects/movieDatabase/movie_database.db') #dasves database in the directory im in 
cursor = movieDat.cursor() #cursor to carry info back and forth 

#create a table and comment code out after the database is created 
# cursor.execute("""
# create table movie_ratings(
#     movie_name text,
#     movie_year int,
#     favourite_actor text,
#     score int
# )
# """)

#make a main frame
mainFrame = LabelFrame(root,pady=10,padx=10,bg='#A877BA')
mainFrame.grid(row =0,column = 0,ipady = 10)
nameOfProgram = Label(mainFrame,text='Movie database',bg='#A877BA',fg = 'white')
nameOfProgram.grid(row = 0,column = 0,columnspan=2)
#second main frame
secondFrame = LabelFrame(root, pady=10,padx=10,bg = '#72A0C1')
secondFrame.grid(row=1,column = 0,ipady=10)
secondFrame_2 = LabelFrame(secondFrame, pady=10,padx=10)
secondFrame_2.grid(row=1,column = 0)
queryLabel = Label(secondFrame,text= 'Search database',pady=10,bg = '#72A0C1',fg = 'white')
queryLabel.grid(row = 0,column = 0,columnspan=2)

#third main frame
thirdFrame = LabelFrame(root, pady=10,padx=10,bg = '#126180')
thirdFrame.grid(row=2,column = 0,ipady=10)
thirdFrame_2 = LabelFrame(thirdFrame, pady=10,padx=10)
thirdFrame_2.grid(row=1,column = 0)
deleteLabel = Label(thirdFrame,text= 'Delete from database',pady=10,bg = '#126180',fg = 'white')
deleteLabel.grid(row = 0,column = 0,columnspan=2)

#make a frame for labels and entry fields
entry_frame = LabelFrame(mainFrame,padx=10,pady=10)
entry_frame.grid(row=1,column=0,columnspan=2)

#frame for results 
results_frame = LabelFrame(root, pady=10,padx=10)
results_frame.grid(row = 0,column=1)

#make textbox labels for the entry fields 
movie_name = Label(entry_frame, text = 'Movie name')
movie_name.grid(row = 1,column=0)
movie_year = Label(entry_frame, text = 'Movie year')
movie_year.grid(row = 2,column=0)
favourite_actor = Label(entry_frame, text = 'Favourite actor')
favourite_actor.grid(row = 3,column=0)
score = Label(entry_frame, text = 'score')
score.grid(row = 4,column=0)

#entry fields
e_movie_name = Entry(entry_frame,width=30)
e_movie_name.grid(row = 1, column=1)
e_movie_year = Entry(entry_frame,width=30)
e_movie_year.grid(row = 2, column=1)
e_favourite_actor = Entry(entry_frame,width=30)
e_favourite_actor.grid(row = 3, column=1)
e_score = Entry(entry_frame,width=30)
e_score.grid(row = 4, column=1)

#submit button
submit_btn = Button(entry_frame,text = 'Add records to database',bg='#54FA9B',fg = 'purple',command=submit)
submit_btn.grid(row= 5,column=0,columnspan=2)

#show all results button
show_all = Button(secondFrame_2,text = 'Show all results',fg = 'purple',command=show_all)
show_all.grid(row=1, column = 0,columnspan=2)

#show result based on oid
e_show_oid = Entry(secondFrame_2,width = 30)
e_show_oid.grid(row=2,column=0)
show_oid = Button(secondFrame_2, text='Show result of ID',command =lambda: showSingleResult(e_show_oid.get()))
show_oid.grid(row=2,column=1)
#update records 
e_update_record = Entry(secondFrame_2,width=30)
e_update_record.grid(row = 3,column=0)
update_record = Button(secondFrame_2,text = 'Update record',command=lambda:updateRecord(e_update_record.get()))
update_record.grid(row =3,column=1)

#delete results based on oid
e_del_oid = Entry(thirdFrame_2,width = 30)
e_del_oid.grid(row=1,column=0)
del_oid = Button(thirdFrame_2, text='Delete entry of ID',command =lambda: deleteSingleResult(e_del_oid.get()))
del_oid.grid(row=1,column=1)

movieDat.commit() #commit changes
movieDat.close() #close the connection

root.mainloop()