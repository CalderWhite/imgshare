<<<<<<< HEAD
# ImgShare, now with Mobile!
=======
# ImgShare
>>>>>>> origin/master
Free, easy image sharing using c9.io
## About
This is a little server written in python that I wrote up in a day    
that allows you to upload images without any account, or fees.    
This server is made to run on [cloud 9](http://c9.io). This is a website    
that essentially allows you to remotely control an unbuntu machine.    
As a cherry on top, c9 gives you teporary hosting (domain name) for free.    
The idea of this project was quick, free and easy. However, c9 does have premium accounts (similar to github and other cloud platforms.)
## Links
My c9 project : https://ide.c9.io/calderwhite/imgshare    
When running, this is the upload domain: https://imgshare-calderwhite.c9users.io
## Usage
### Backend (Terminal)
From the backend all there is to do is run the file.
#### Execution
To run, enter the imgshare directory and then run:    
`python3 c9Server.py`
### Browser (Client)
From a Browser you can upload, and view (download) images.
#### Viewing
In order to view an image from a web page (when server running), here's how:    
`https://imgshare-<username>.c9users.io/userData/userFiles/<user's ip>/<filename>`
#### Uploading
Uploading is rather simple, just go to the base domain:    
`https://imgshare-<username>/c9users.io`
