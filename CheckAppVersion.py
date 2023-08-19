import paramiko
import time
import csv
import subprocess

with open('CheckApppy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    log_file = "error_log.txt"

    for row in reader:
        try:
            if len(row) < 3:
                print("islem tamamlandi.")
                break

            userName = "winrmuser"
            passWord = 'c9!$8b#r9jz2X7k'
            print(row[0])
            print(row[1])
            print(row[2])
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(row[0], 22, userName, passWord)
            stdin, stdout, stderr = ssh.exec_command('whoami')
            time.sleep(1)
            print(stdout.read())
            user2 = row[1]
            script = row[2]
            stdin, stdout, stderr = ssh.exec_command(f'dzdo su - {user2}', get_pty=True)
            time.sleep(1)
            stdin.write('whoami\n')
            stdin.write(f'whoami;pwd;{script};exit;\n')
            stdin.flush()
       
            
            error_output = stdout.readlines()
            found_no = False
            for line in error_output:
                if "No" in line:
                    found_no = True
                    break

            if found_no:
                print("error olarak logladi!")
                with open(log_file, 'a') as log:
                    log.write(f"Sunucu: {row[0]}, Kullanıcı: {row[1]}, Komut: {script} - Hata: {error_output}\n")

            print(error_output)
            ssh.close()

        except Exception as e:
            print(f"Hata: {e}")
            with open(log_file, 'a') as log:
              log.write(f"Sunucu: {row[0]}, Kullanıcı: {row[1]}, Komut: {row[2]} - Hata: {e} \n")
            continue
