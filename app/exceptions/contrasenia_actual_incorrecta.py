class contrasenia_actual_incorrecta(ValueError): 
    
    def __init__(self, value):
        self.value= value
        self.code="CONTRASENIA-ACTUAL-INCORRECTA"
        super().__init__("La contrasenia actual ingresada es incorrecta.")