#Evin Weissenberg

def save_image(self,image_url):


		try:
			#get string length, if it fails raise an exception
			len(image_url)

		except Exception as e:
			print('There was an error processing image.')
			raise
		else:
			#generate a global unique ID (avoids conflicts with other file names.)
			image_name = str(uuid.uuid4())		
			#get image data in assign it to a variable					
			response = requests.get(image_url, stream=True)		
			
			#extension detection
			content_type = response.headers['content-type']
			extension = mimetypes.guess_extension(content_type)
			
			#combining the new GUID name with the extension to build its identity
			new_image_name = image_name+extension
			#save to local directory
			with open('/path/to/saved/image/'+new_image_name, 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			#delete old response data
			del response		

			#create on the fly ssh known_host or use your own below
			ssh = paramiko.SSHClient() 		
			# ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))		
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			#Connect to the server you want to copy new file
			ssh.connect('1.1.1.1', username='user', password='password')
			sftp = ssh.open_sftp()
			#copy from current local server to new server
			sftp.put('/path/to/saved/image/'+new_image_name, '/path/to/new/server/directory/'+new_image_name)
			sftp.close()
			ssh.close()	

			#return new image name
			return new_image_name
			
		finally:
			pass

