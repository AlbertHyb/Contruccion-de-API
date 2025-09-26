from recursos import HelloWorld, InicioDeSesion, RegistroUsuario



class RutasAPI:
    #Recibe el lugar donde estaran disponibles las rutas
    def inicializar_rutas(self, api):
      api.add_resource(HelloWorld, '/')
      api.add_resource(InicioDeSesion, '/login')
      api.add_resource(RegistroUsuario, '/signup')