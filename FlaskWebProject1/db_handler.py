import hashlib
import pypyodbc
import random
import string


"""Database information"""
driver = "{ODBC Driver 13 for SQL Server}"
server = "tcp:flasking.database.windows.net,1433"
db_name = "flasking-db"
uid = "bob@flasking"
pwd = "flaskingDB24"


def get_connection():
	"""Establishes connection to database."""
	return pypyodbc.connect(
		driver=driver,
		server=server,
		database=db_name,
		uid=uid,
		pwd=pwd
	)


def user_exists(_email):
	"""Checks if user is already present in database."""
	exists = False

	query = "SELECT * FROM CREDENTIALS " \
				+ "WHERE LTRIM(RTRIM(Email))=LTRIM(RTRIM(?))"
	values = (_email, )

	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(query, values)
	if len(cursor.fetchall()) > 0:
		exists = True
	conn.close()

	return exists


def insert_user(_email, _password):
	"""Inserts user into database."""
	# generate salt and prepend it to user's password
	salt = generate_salt()
	result = salt + _password

    # build hash
	hash_builder = hashlib.md5()
	encoding = result.encode("utf-8")
	hash_builder.update(encoding)
	result = hash_builder.hexdigest()

	# insert into database
	query = "INSERT INTO Credentials " \
		+ "(Email, Hash, Salt) " \
		+ "VALUES (?, ?, ?)"
	values = (_email, result, salt)

	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(query, values)
	conn.commit()
	conn.close()


def generate_salt(size=6, chars=string.ascii_uppercase + string.digits):
    """Random salt generator. Used to safely store passwords."""
    return ''.join(random.choice(chars) for _ in range(size))


def check_credentials(_email, _password):
	"""Checks credentials for logging in"""
	query = "SELECT Hash, Salt FROM CREDENTIALS "\
				+ "WHERE LTRIM(RTRIM(Email))=LTRIM(RTRIM(?))"
	values = (_email, )

	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(query, values)
	result = cursor.fetchone()
	conn.close()

	if result is None:
		# user does not exist
		return False

	expected_hash = result[0]
	salt          = result[1]
	
	# prepend salt to password
	aux = salt + _password

	# compute hash value
	hash_builder = hashlib.md5()
	encoding = aux.encode("utf-8")
	hash_builder.update(encoding)
	current_hash = hash_builder.hexdigest()

	# check hashes
	if expected_hash != current_hash:
		# passwords don't match
		return False

	# all good!
	return True
