class mail_eliminado(ValueError): 
    
    def __init__(self, value):
        self.value= value
        self.code= "MAIL-ELIMINADO-ERROR"
        
        super().__init__("El mail no se puede utilizar")