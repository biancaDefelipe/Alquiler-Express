class envio_mail_error(ValueError): 
    
    def __init__(self, value):
        self.value= value
        self.code="ENVIO-MAIL-ERROR"
        super().__init__("No se pudo enviar el mail ")