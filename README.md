

# Blog-Website

Personal Website on https://eliyahumasinter.com built using the Python module Flask.

# Why I built the website
I built the core of this website on the plane ride from America to Israel. 
The purpose of the website is to be a blog about my stay in Israel so that I don't have to write the same email and have the same conversation with a dozen different people. I can simply send them a link to my website.

# How it works
**Backend** 
I can control all aspects of the website from my admin page. Writing posts (including uploading images), manually add and delete emails from the notification list,  edit/remove posts, and send out a notification to everyone in the notification list. 
**Front end**
I originally challenged myself to write all of the CSS myself, but as of December of 2021, I'm planning on implementing Bootstrap into the website to make it more mobile friendly. In addition to the mobile version of the website, Bootstrap has other features I plan on using including modals and there icon library.  
# Main Modules Used
* flask
		 The brunt of the site was built using Flask. 
	* flask_bootstrap
	  Used for front-end work (navbar, mobile site, etc.)
	* flask_sqlalchemy
	  Convenient module for working with SQL databases in Flask designed to work with the sqlalchemy module
	* flask_basicauth
	  Authentication for the admin page
* sqlalchemy
Used in sync with flask_sqlalchemy to easily read and write to SQL databases (SQLite3 in my case).
* PIL
Used for optimizing pictures and converting them to jpg.
* datetime
format and calculate dates for each post
* werkzeug
Make sure all files uploaded have a safe name using the secure_file function from werkzeug.utils.
* smtplib
 for sending email notifications. 
# Future Plans
The website already does what I originally intended, but there's always more I could add. Currently (as of December of 2021), I'm working on adding a like feature to the website so that those who signed up for notifications can like posts.
