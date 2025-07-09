class dni_invalido(ValueError): 
    
    def __init__(self, value):
        self.value= value
        self.code="DNI-ERROR"
        super().__init__("El DNI ya está registrado")