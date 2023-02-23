from cryptography.fernet import Fernet
with open('x64/dll.key')as f:
    key=f.read().encode()
x=Fernet(key)

in_dir=input('Enter the directory to the source code: '); out_dir=input('Enter the output filename: ')
with open(in_dir)as f:
    code=f.read()

output=''
for c in code.split('\n'):
    output=f'{output}{x.encrypt(c.encode()).decode()}\n'

with open(out_dir, 'w')as f:
    f.write(output)