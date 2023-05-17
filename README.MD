Blog project
This is a django project
that includes 3 different apps to manage posts and comments

structure

    simple_social
        |-- accounts
        |-- groups
        |-- posts
        |-- simple_social
        | manage.py

was implemented using class-based views and class-bases generic views methodology.
It is an adapted version of a blog project implemented in django 1.1

# to run the server: python manage.py runserver

TODOS: 
1. make sure support groups and post can be made using Japanese
2. create a list of upcoming events than will show up in a sidebar next to de group details
3. create a user information interface, must be accessible by users to modify their own information
4. Delete the old picture stored after update a post with a new picture
5. create a simple small space to load bluprint pictures in the group details page