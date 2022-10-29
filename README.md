### The Django project - BBoard. 
The application suggest functionality of a bulletin board for a community.
The following functionality is implemented:
1) registration by e-mail with the registration confirmation code;
2) creating and editing bulletins;
3) bulletins consist of a title and text, inside which there may be pictures, embedded videos and other content;
4) registered users can leave comments for other users;
5) e-mail notification of a change in the status of comments;
6) user's personal account for editing bulletins and comments to them;
7) editable list of categories.

To configure sending emails via Celery and Redis, use the USE_CELERY_SEND_EMAIL variable

