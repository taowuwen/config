
### This adds a new user and password
	rabbitmqctl add_user username password
### This makes the user a administrator
	rabbitmqctl set_user_tags username administrator
### This sets permissions for the user
	rabbitmqctl set_permissions -p / username ".*" ".*" ".*"
