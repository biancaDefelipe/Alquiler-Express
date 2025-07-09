class mail_invalido(ValueError): 
    
    def __init__(self, value):
        self.value= value
        self.code= "MAIL-ERROR"
        
        super().__init__("El mail ya está registrado")