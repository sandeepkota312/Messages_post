This API should allow users to: 
1. Post a new message 
2. View a list of all messages, with the most recent messages first 
3. Like a message by clicking a button 
4. View the total number of likes for each message
5. Edit/DELETE the post
6. Also created a rest API for the same

Instructions:
1. clone the resources into your local machine
2. create a virtual environment in the parent directory
3. install the packages mentioned in requirements.txt
4. also create a database and name it as 'messagesDB' in postgresql or using pgadmin gui application, creating a default user as 'postgres' with password '1234' and port ='5432' in general
5. go to messages_app directory and create a superuser.
6. then migrate the contents into the database - 'python manage.py makemigrations' then 'python manage.py migrate'
8. run the server using 'python manage.py runserver'
9. create an account and login
10. from there you will have a set of url directories for the mentioned functionality attached(create a post, post list, like a post, modify a post, delete a post)


