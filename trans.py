import subprocess
from tokenize import String

class Courier:
   def __init__(self, backend):
      self.backend = backend
      self.pipe = subprocess.Popen(backend, bufsize=1024, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   
   def read(self):
      ret = ''
      while True:
         nowline = self.pipe.stdout.readline().decode('UTF-8')
         if nowline == "__end_of_output__\n":
            break
         else:
            ret += nowline
      print('read:', ret)
      return ret

   def write(self, str):
      print('write:', str)
      self.pipe.stdin.write((str + '\n').encode('UTF-8'))
      self.pipe.stdin.flush()

   def add(self, a, b):
      self.write(str(a) + ' ' + str(b))
      res = int(self.read())
      return res

   def login(self, us, ps):
      self.write('[0] login -u ' + us + ' -p ' + ps)
      res = int(self.read())
      return res

   def add_user(self, c, u, p, n, m, g):
      self.write('[0] add_user -c ' + c + ' -u ' + u + ' -p ' + p + ' -n ' + n + ' -m ' + m + ' -g ' + str(g))
      res = int(self.read())
      return res
   
   def add_user2(self, s):
      self.write(s)
      res = int(self.read())
      return res


   def login(self, u, p):
      self.write('[0] login -u ' + u + ' -p ' + p)
      res = int(self.read())
      return res

   def logout(self, u):
      self.write('[0] logout -u ' + u)
      res = int(self.read())
      return res

   def query_profile(self, c, u):
      print('[0] query_profile -c ' + c + ' -u ' + u)
      self.write('[0] query_profile -c ' + c + ' -u ' + u)
      st = self.read()
      res = st.split()
      return res
   
   def modify_user(self, s):
      print(s)
      self.write(s)
      st = self.read()
      res = st.split()
      return res