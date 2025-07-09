class dni_eliminado(ValueError): 
    
    def __init__(self, value):
        self.value= value
        self.code= "DNI-ELIMINADO-ERROR"
        
        super().__init__("El dni no se puede utilizar")