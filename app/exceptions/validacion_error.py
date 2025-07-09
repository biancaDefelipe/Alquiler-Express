class validacion_error(ValueError): 
    
    def __init__(self):
        self.code= "VALIDACION-ERROR"
        self.validacion= False
        
        super().__init__("Los datos ingresados no coinciden")