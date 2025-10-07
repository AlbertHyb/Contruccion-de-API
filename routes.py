from recursos import (HelloWorld, InicioDeSesion, RegistroUsuario, 
                      PerfilUsuario, RefreshToken, Logout)



class RutasAPI:
    #Recibe el lugar donde estaran disponibles las rutas
    def inicializar_rutas(self, api):
      api.add_resource(HelloWorld, '/')
      api.add_resource(InicioDeSesion, '/login')
      api.add_resource(RegistroUsuario, '/signup')
      
      # Rutas protegidas
      api.add_resource(PerfilUsuario, '/profile')
      api.add_resource(RefreshToken, '/refresh')
      api.add_resource(Logout, '/logout')


